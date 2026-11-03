"""Feature engineering shared by training and serving (one code path, no train/serve skew)."""
from __future__ import annotations

import numpy as np
import pandas as pd

SENSORS = [f"s{i}" for i in range(1, 22)]


def add_rul(df: pd.DataFrame, cap: int | None = 125) -> pd.DataFrame:
    """Remaining useful life target per row; piecewise-linear cap (common practice on C-MAPSS)."""
    out = df.copy()
    max_cycle = out.groupby("unit")["cycle"].transform("max")
    out["rul"] = max_cycle - out["cycle"]
    if cap is not None:
        out["rul"] = out["rul"].clip(upper=cap)
    return out


def informative_sensors(train: pd.DataFrame, min_std: float = 1e-4) -> list[str]:
    """Drop (near-)constant sensors, decided on TRAIN only."""
    std = train[SENSORS].std()
    return [s for s in SENSORS if std[s] > min_std]


def rolling_features(df: pd.DataFrame, sensors: list[str], windows: tuple[int, ...] = (5, 15)) -> pd.DataFrame:
    """Per-unit rolling mean/std + slope proxies. Uses only past and current cycles (causal)."""
    df = df.sort_values(["unit", "cycle"]).reset_index(drop=True)
    g = df.groupby("unit", group_keys=False)
    feats = {"cycle": df["cycle"]}
    for s in sensors:
        feats[s] = df[s]
        for w in windows:
            feats[f"{s}_mean{w}"] = g[s].transform(lambda x, w=w: x.rolling(w, min_periods=1).mean())
            feats[f"{s}_std{w}"] = g[s].transform(lambda x, w=w: x.rolling(w, min_periods=2).std()).fillna(0.0)
        feats[f"{s}_diff{windows[-1]}"] = df[s] - g[s].transform(lambda x: x.shift(windows[-1])).fillna(df[s])
    X = pd.DataFrame(feats)
    X.insert(0, "unit", df["unit"].to_numpy())
    return X


def last_cycle_rows(X: pd.DataFrame) -> pd.DataFrame:
    """Rows at the last observed cycle of each unit (test-set protocol)."""
    idx = X.groupby("unit")["cycle"].idxmax()
    return X.loc[idx].sort_values("unit").reset_index(drop=True)


def feature_columns(X: pd.DataFrame) -> list[str]:
    return [c for c in X.columns if c not in ("unit", "rul")]


def healthy_mask(df: pd.DataFrame, frac: float = 0.3) -> np.ndarray:
    """True for the first `frac` of each unit's life — assumed healthy, used to fit the anomaly detector."""
    max_cycle = df.groupby("unit")["cycle"].transform("max")
    return (df["cycle"] <= frac * max_cycle).to_numpy()
