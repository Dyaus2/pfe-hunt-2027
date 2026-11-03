"""Prequential simulation of three maintenance strategies on a labelled stream:

- static:          train once, never retrain
- periodic:        retrain every `period` batches, promote if gates pass
- champion_challenger: retrain when drift (PSI) or a performance drop is detected; the challenger runs in
                   shadow for `shadow` batches and is promoted only if it beats the champion; automatic
                   rollback if the new champion underperforms right after promotion.

Each batch: (1) score with the current champion, (2) labels arrive, (3) log metrics, (4) maybe act.
The PSI reference is refreshed only on promotion (from data the promoted model was trained on), so a
slowly poisoned stream cannot silently move the reference.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

from .drift import drift_flag, feature_psi
from .gates import QualityGates, safe_auc
from .registry import ModelRegistry


def default_model(seed: int = 0):
    return HistGradientBoostingClassifier(max_iter=150, learning_rate=0.08, random_state=seed)


@dataclass
class LoopConfig:
    strategy: str = "champion_challenger"   # static | periodic | champion_challenger
    window: int = 8                          # batches used to (re)train
    period: int = 4                          # periodic strategy
    shadow: int = 2                          # batches a challenger runs in shadow
    psi_threshold: float = 0.2
    perf_drop: float = 0.05                  # trigger if rolling AUC < reference AUC - perf_drop
    promote_margin: float = 0.0
    rollback_delta: float = 0.05
    cooldown: int = 2                        # batches between triggers
    seed: int = 0


def run_stream(batch_list: list[tuple[pd.DataFrame, np.ndarray]], cfg: LoopConfig, registry_dir: str,
               model_factory=default_model, gates: QualityGates | None = None) -> pd.DataFrame:
    gates = gates or QualityGates()
    reg = ModelRegistry(registry_dir)
    W = cfg.window
    hist_X = [b[0] for b in batch_list[:W]]
    hist_y = [b[1] for b in batch_list[:W]]

    def fit_on(Xs, ys):
        return model_factory(cfg.seed).fit(pd.concat(Xs, ignore_index=True), np.concatenate(ys))

    champ = fit_on(hist_X, hist_y)
    v = reg.register(champ, {"trained_on_batches": [0, W - 1]})
    reg.promote(v, "initial")
    reference = pd.concat(hist_X, ignore_index=True)
    ref_auc = None
    challenger, challenger_v, shadow_scores, challenger_ref = None, None, [], None
    prev_state = None  # (reference, ref_auc) before the last promotion, restored on rollback
    last_trigger, prev_champ_auc_on_shadow, just_promoted = -10, None, False
    logs = []

    for t in range(W, len(batch_list)):
        X, y = batch_list[t]
        p = champ.predict_proba(X)[:, 1]
        auc = safe_auc(y, p)
        acc = float(((p >= 0.5).astype(int) == y).mean())
        psis = feature_psi(reference, X)
        drift = drift_flag(psis, cfg.psi_threshold)
        row = {"batch": t, "auc": auc, "acc": acc, "psi_max": max(psis.values()), "psi_top": max(psis, key=psis.get), "drift": drift,
               "champion": reg.champion, "retrained": False, "promoted": False, "rolled_back": False, "gate_fail": ""}
        ref_auc = auc if ref_auc is None else ref_auc

        # post-promotion safety net
        if just_promoted and prev_champ_auc_on_shadow is not None and auc < prev_champ_auc_on_shadow - cfg.rollback_delta:
            back = reg.rollback(f"auc {auc:.3f} after promotion")
            if back is not None:
                champ = reg.load(back)
                reference, ref_auc = prev_state
                row["rolled_back"] = True
        just_promoted = False

        # shadow evaluation of a pending challenger
        if challenger is not None:
            shadow_scores.append((auc, safe_auc(y, challenger.predict_proba(X)[:, 1])))
            if len(shadow_scores) >= cfg.shadow:
                ch_mean = np.nanmean([s[1] for s in shadow_scores])
                cp_mean = np.nanmean([s[0] for s in shadow_scores])
                if ch_mean >= cp_mean + cfg.promote_margin:
                    reg.promote(challenger_v, f"shadow auc {ch_mean:.3f} vs {cp_mean:.3f}")
                    prev_state = (reference, ref_auc)
                    champ, row["promoted"], just_promoted = challenger, True, True
                    prev_champ_auc_on_shadow, ref_auc = cp_mean, ch_mean
                    reference = challenger_ref  # data the promoted model was trained on
                challenger, challenger_v, shadow_scores, challenger_ref = None, None, [], None

        hist_X.append(X)
        hist_y.append(y)

        # decide whether to (re)train
        trigger = False
        if cfg.strategy == "periodic":
            trigger = (t - W + 1) % cfg.period == 0
        elif cfg.strategy == "champion_challenger" and challenger is None and t - last_trigger >= cfg.cooldown:
            recent = [r["auc"] for r in logs[-1:]] + [auc]
            perf_bad = np.nanmean(recent) < ref_auc - cfg.perf_drop
            trigger = drift or perf_bad
        if trigger:
            last_trigger = t
            cand = fit_on(hist_X[-W - 1:-1], hist_y[-W - 1:-1])  # hold out the newest batch for the gates
            pc = cand.predict_proba(X)[:, 1]
            ok, reasons = gates.check(y, pc, champion_auc=None if cfg.strategy != "periodic" else auc)
            row["retrained"] = True
            if not ok:
                row["gate_fail"] = "; ".join(reasons)
            else:
                cand = fit_on(hist_X[-W:], hist_y[-W:])  # refit including newest batch
                cv = reg.register(cand, {"gate_auc": safe_auc(y, pc), "trained_upto": t})
                if cfg.strategy == "periodic":
                    reg.promote(cv, "periodic")
                    champ, row["promoted"] = cand, True
                    reference = pd.concat(hist_X[-W:], ignore_index=True)
                else:
                    challenger, challenger_v, shadow_scores = cand, cv, []
                    challenger_ref = pd.concat(hist_X[-W:], ignore_index=True)
        logs.append(row)
    return pd.DataFrame(logs)


def summarize(log: pd.DataFrame) -> dict:
    return {"mean_auc": float(log["auc"].mean()), "mean_acc": float(log["acc"].mean()),
            "retrains": int(log["retrained"].sum()), "promotions": int(log["promoted"].sum()),
            "rollbacks": int(log["rolled_back"].sum()), "drift_batches": int(log["drift"].sum())}
