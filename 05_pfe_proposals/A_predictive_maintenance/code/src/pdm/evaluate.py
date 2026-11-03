"""Metrics: RMSE, the PHM08 asymmetric score (late predictions penalised more), alarm lead time."""
from __future__ import annotations

import numpy as np
import pandas as pd


def rmse(y_true, y_pred) -> float:
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    return float(np.sqrt(np.mean((y_pred - y_true) ** 2)))


def phm08_score(y_true, y_pred) -> float:
    """Saxena et al. 2008 scoring: d = pred - true; exp(-d/13)-1 if d<0 (early), exp(d/10)-1 if d>=0 (late)."""
    d = np.asarray(y_pred, float) - np.asarray(y_true, float)
    return float(np.sum(np.where(d < 0, np.exp(-d / 13.0) - 1.0, np.exp(d / 10.0) - 1.0)))


def alarm_lead_times(df: pd.DataFrame, alarm: pd.Series) -> pd.DataFrame:
    """Per unit: first alarm cycle and lead time (cycles before failure). NaN lead time = missed failure."""
    out = []
    for u, g in df.assign(alarm=alarm.to_numpy()).groupby("unit"):
        life = int(g["cycle"].max())
        hits = g.loc[g["alarm"], "cycle"]
        first = int(hits.min()) if len(hits) else np.nan
        out.append({"unit": u, "life": life, "first_alarm": first,
                    "lead_time": (life - first) if len(hits) else np.nan})
    return pd.DataFrame(out)


def alarm_summary(lead: pd.DataFrame, too_early: int = 100) -> dict:
    """Detection rate, median lead time, share of 'too early' alarms (likely false alarms)."""
    detected = lead["lead_time"].notna()
    return {
        "units": int(len(lead)),
        "detection_rate": float(detected.mean()),
        "median_lead_time": float(lead.loc[detected, "lead_time"].median()) if detected.any() else float("nan"),
        "too_early_rate": float((lead["lead_time"] > too_early).mean()),
    }
