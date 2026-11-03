"""Offline quality gates a candidate must pass before it may challenge the champion."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.metrics import roc_auc_score


def safe_auc(y, p) -> float:
    return float(roc_auc_score(y, p)) if len(np.unique(y)) == 2 else float("nan")


def ece(y, p, bins: int = 10) -> float:
    """Expected calibration error with equal-width bins."""
    y, p = np.asarray(y, float), np.asarray(p, float)
    idx = np.minimum((p * bins).astype(int), bins - 1)
    total = 0.0
    for b in range(bins):
        m = idx == b
        if m.any():
            total += m.mean() * abs(y[m].mean() - p[m].mean())
    return float(total)


@dataclass
class QualityGates:
    min_auc: float = 0.6
    max_ece: float = 0.15
    max_auc_drop_vs_champion: float = 0.02
    min_rows: int = 200

    def check(self, y, p, champion_auc: float | None = None) -> tuple[bool, list[str]]:
        reasons = []
        if len(y) < self.min_rows:
            reasons.append(f"too few rows ({len(y)} < {self.min_rows})")
        if not np.isfinite(p).all():
            reasons.append("non-finite predictions")
        auc = safe_auc(y, p)
        if not (auc >= self.min_auc):
            reasons.append(f"AUC {auc:.3f} < {self.min_auc}")
        e = ece(y, p)
        if e > self.max_ece:
            reasons.append(f"ECE {e:.3f} > {self.max_ece}")
        if champion_auc is not None and np.isfinite(champion_auc) and auc < champion_auc - self.max_auc_drop_vs_champion:
            reasons.append(f"AUC {auc:.3f} worse than champion {champion_auc:.3f}")
        return (not reasons), reasons
