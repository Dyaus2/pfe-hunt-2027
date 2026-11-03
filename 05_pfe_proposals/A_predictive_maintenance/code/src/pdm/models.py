"""Baseline models: RUL regression (gradient boosting) + unsupervised health monitoring (Isolation Forest)."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor, IsolationForest
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def make_rul_model(seed: int = 0) -> HistGradientBoostingRegressor:
    return HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, max_leaf_nodes=31,
                                         l2_regularization=1.0, random_state=seed)


@dataclass
class HealthMonitor:
    """Isolation Forest fitted on healthy cycles; raises an alarm after `k` consecutive anomalous cycles."""
    n_estimators: int = 300
    contamination: float = 0.02
    k: int = 5
    seed: int = 0

    def fit(self, X_healthy: pd.DataFrame) -> "HealthMonitor":
        self.cols_ = list(X_healthy.columns)
        self.model_ = make_pipeline(StandardScaler(), IsolationForest(
            n_estimators=self.n_estimators, contamination=self.contamination, random_state=self.seed))
        self.model_.fit(X_healthy.to_numpy())
        return self

    def anomaly_score(self, X: pd.DataFrame) -> np.ndarray:
        """Higher = more anomalous."""
        return -self.model_.decision_function(X[self.cols_].to_numpy())

    def alarms(self, X: pd.DataFrame, units: pd.Series) -> pd.Series:
        """Boolean alarm per row: anomalous for k consecutive cycles within the same unit."""
        flag = pd.Series(self.model_.predict(X[self.cols_].to_numpy()) == -1, index=X.index)
        run = flag.groupby(units.to_numpy()).transform(lambda f: f.astype(int).rolling(self.k, min_periods=self.k).sum())
        return (run >= self.k).fillna(False)
