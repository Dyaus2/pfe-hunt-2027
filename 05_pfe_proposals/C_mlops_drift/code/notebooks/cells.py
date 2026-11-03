TITLE = """# PFE proposal C — MLOps: drift monitoring + champion/challenger retraining with rollback
Prequential simulation on a real non-stationary stream (Elec2 electricity market, OpenML id 151), in weekly batches.
Compares **static**, **periodic retraining** and **drift-triggered champion/challenger** (shadow trial, quality gates, automatic rollback).
CPU only, ~3 minutes."""
PIP = "scikit-learn pandas numpy matplotlib joblib"

CELLS = [
("code", """import tempfile, pandas as pd
from driftops import data
from driftops.loop import LoopConfig, run_stream, summarize
try:
    X, y = data.load_electricity(); SOURCE = 'Elec2 (OpenML 151)'; SIZE = 336
except Exception as e:
    print('OpenML unavailable, synthetic stream:', e)
    X, y = data.make_synthetic_stream(60, 300, drift_at=30); SOURCE = 'synthetic'; SIZE = 300
B = list(data.batches(X, y, SIZE)); print(SOURCE, len(B), 'batches')"""),
("code", """logs = {s: run_stream(B, LoopConfig(strategy=s, window=8, period=4), tempfile.mkdtemp())
        for s in ['static', 'periodic', 'champion_challenger']}
pd.DataFrame({s: summarize(l) for s, l in logs.items()}).T"""),
("code", """import matplotlib.pyplot as plt
plt.figure(figsize=(10, 3.5))
for s, l in logs.items():
    plt.plot(l['batch'], l['auc'].rolling(4, min_periods=1).mean(), label=s)
cc = logs['champion_challenger']
for b in cc.loc[cc['promoted'], 'batch']: plt.axvline(b, color='green', alpha=.15)
for b in cc.loc[cc['rolled_back'], 'batch']: plt.axvline(b, color='red', alpha=.4)
plt.ylabel('AUC (4-batch rolling)'); plt.xlabel('week'); plt.legend(); plt.title(f'{SOURCE}: green = promotion, red = rollback'); plt.tight_layout(); plt.show()"""),
("md", """### Alert fatigue: PSI on raw, autocorrelated features fires almost every week
One week of prices/demand is a narrow slice compared with an 8-week reference, so PSI is large even without a real concept change (median PSI ≈ 2.6 on this stream).
PFE question: which drift signal is *actionable*? Options: monitor the model-score distribution or residuals, use seasonal references, require multi-feature agreement."""),
("code", """cc[['psi_top']].value_counts().rename('batches where feature had max PSI').to_frame()"""),
("code", """rows = []
for thr in [0.5, 2.0, 5.0]:
    l = run_stream(B, LoopConfig(strategy='champion_challenger', window=8, psi_threshold=thr), tempfile.mkdtemp())
    rows.append({'psi_threshold': thr, **summarize(l)})
pd.DataFrame(rows)"""),
("md", """## Next steps for the PFE
1. Replace the stream with the host's model inputs + delayed labels; plug the registry into MLflow.
2. Add label-free performance estimation for when labels arrive late, plus per-segment monitoring.
3. Wire it as a scheduled pipeline (Airflow/Prefect or GitHub Actions) with a dashboard and alert routing."""),
]
