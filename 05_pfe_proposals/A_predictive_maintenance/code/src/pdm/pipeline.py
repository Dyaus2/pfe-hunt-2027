"""End-to-end baseline: features → RUL model (unit-grouped validation) → test protocol → health monitor."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold

from . import evaluate as ev
from . import features as fe
from .models import HealthMonitor, make_rul_model


def _random_cut_rows(X: pd.DataFrame, rng: np.random.Generator, per_unit: int = 5, min_frac: float = 0.3) -> pd.DataFrame:
    """Sample `per_unit` rows per unit between min_frac of life and failure. Features are causal, so a row's
    features equal those computed on the series truncated at that row."""
    picks = []
    for _, g in X.groupby("unit"):
        lo = int(min_frac * len(g))
        picks.extend(rng.choice(g.index[lo:], size=min(per_unit, len(g) - lo), replace=False))
    return X.loc[picks]


def run_baseline(train: pd.DataFrame, test: pd.DataFrame, rul_test: np.ndarray, cap: int = 125,
                 n_splits: int = 5, seed: int = 0) -> dict:
    sensors = fe.informative_sensors(train)
    tr = fe.add_rul(train, cap=cap)
    Xtr = fe.rolling_features(tr, sensors)
    Xtr["rul"] = tr.sort_values(["unit", "cycle"])["rul"].to_numpy()
    cols = fe.feature_columns(Xtr)

    # 1) cross-validation grouped by engine (no leakage across cycles of the same unit)
    cv_rmse = []
    rng = np.random.default_rng(seed)
    for tr_idx, va_idx in GroupKFold(n_splits=n_splits).split(Xtr, groups=Xtr["unit"]):
        m = make_rul_model(seed).fit(Xtr.iloc[tr_idx][cols], Xtr.iloc[tr_idx]["rul"])
        va = Xtr.iloc[va_idx]
        pts = _random_cut_rows(va, rng)  # mimic the test protocol: score at random points of life, not at failure
        cv_rmse.append(ev.rmse(pts["rul"], m.predict(pts[cols])))

    # 2) final model → official test protocol (prediction at last observed cycle)
    model = make_rul_model(seed).fit(Xtr[cols], Xtr["rul"])
    Xte = fe.last_cycle_rows(fe.rolling_features(test, sensors))
    pred = np.clip(model.predict(Xte[cols]), 0, None)
    y = np.minimum(rul_test, cap)

    # 3) unsupervised health monitor fitted on early-life cycles only
    tr_sorted = train.sort_values(["unit", "cycle"]).reset_index(drop=True)
    healthy = fe.healthy_mask(tr_sorted)
    mon_cols = [c for c in cols if c != "cycle"]
    mon = HealthMonitor(seed=seed).fit(Xtr.loc[healthy, mon_cols])
    alarm = mon.alarms(Xtr[mon_cols], Xtr["unit"])
    lead = ev.alarm_lead_times(tr_sorted, alarm)

    return {
        "sensors_used": sensors,
        "cv_rmse_mean": float(np.mean(cv_rmse)),
        "cv_rmse_std": float(np.std(cv_rmse)),
        "test_rmse": ev.rmse(y, pred),
        "test_phm08_score": ev.phm08_score(y, pred),
        "alarms_on_train_units": ev.alarm_summary(lead),  # in-sample diagnostic; use held-out units in the PFE
        "predictions": pd.DataFrame({"unit": Xte["unit"], "rul_true": y, "rul_pred": pred}),
    }
