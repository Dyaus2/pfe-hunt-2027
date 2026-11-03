"""Streams for drift experiments.

Real: 'electricity' (Elec2, NSW market 1996–1998), OpenML data_id=151 — https://www.openml.org/d/151
Synthetic: logistic concept with an abrupt rotation + covariate shift (for tests).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

FEATURES = ["day", "period", "nswprice", "nswdemand", "vicprice", "vicdemand", "transfer"]


def load_electricity(data_home: str | None = None) -> tuple[pd.DataFrame, np.ndarray]:
    from sklearn.datasets import fetch_openml
    d = fetch_openml(data_id=151, as_frame=True, data_home=data_home, parser="auto")
    df = d.frame
    X = df[FEATURES].astype(float).reset_index(drop=True)
    y = (df["class"].astype(str) == "UP").astype(int).to_numpy()
    return X, y  # rows are already in time order (half-hourly)


def batches(X: pd.DataFrame, y: np.ndarray, size: int = 336):
    """Yield consecutive (X_batch, y_batch). 336 half-hours = 1 week."""
    for s in range(0, len(X) - size + 1, size):
        yield X.iloc[s:s + size].reset_index(drop=True), y[s:s + size]


def make_synthetic_stream(n_batches: int = 40, size: int = 300, drift_at: int = 20, n_features: int = 5,
                          seed: int = 0) -> tuple[pd.DataFrame, np.ndarray]:
    rng = np.random.default_rng(seed)
    w_before = rng.normal(0, 1, n_features)
    w_after = -w_before + rng.normal(0, 0.3, n_features)  # concept flips
    Xs, ys = [], []
    for b in range(n_batches):
        shift = 1.0 if b >= drift_at else 0.0             # covariate shift on feature 0
        X = rng.normal(0, 1, (size, n_features))
        X[:, 0] += shift
        w = w_after if b >= drift_at else w_before
        p = 1 / (1 + np.exp(-(X @ w)))
        Xs.append(X)
        ys.append((rng.random(size) < p).astype(int))
    X = pd.DataFrame(np.vstack(Xs), columns=[f"x{i}" for i in range(n_features)])
    return X, np.concatenate(ys)
