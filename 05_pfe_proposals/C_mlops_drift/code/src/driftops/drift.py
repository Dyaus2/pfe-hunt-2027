"""Population Stability Index per feature (bins = reference quantiles)."""
from __future__ import annotations

import numpy as np
import pandas as pd


def psi(ref: np.ndarray, cur: np.ndarray, bins: int = 10, eps: float = 1e-4) -> float:
    ref, cur = np.asarray(ref, float), np.asarray(cur, float)
    edges = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))
    if len(edges) < 3:  # (near-)constant reference: compare share of values equal to the reference value
        same_ref, same_cur = np.mean(ref == ref[0]), np.mean(cur == ref[0])
        p, q = np.array([same_ref, 1 - same_ref]) + eps, np.array([same_cur, 1 - same_cur]) + eps
        return float(np.sum((q - p) * np.log(q / p)))
    edges[0], edges[-1] = -np.inf, np.inf
    p = np.histogram(ref, edges)[0] / len(ref) + eps
    q = np.histogram(cur, edges)[0] / len(cur) + eps
    return float(np.sum((q - p) * np.log(q / p)))


def feature_psi(ref: pd.DataFrame, cur: pd.DataFrame, bins: int = 10) -> dict[str, float]:
    return {c: psi(ref[c].to_numpy(), cur[c].to_numpy(), bins) for c in ref.columns}


def drift_flag(psis: dict[str, float], threshold: float = 0.2, min_features: int = 1) -> bool:
    """Rule of thumb: PSI < 0.1 stable, 0.1–0.2 moderate, > 0.2 significant shift."""
    return sum(v > threshold for v in psis.values()) >= min_features
