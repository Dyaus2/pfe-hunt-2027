TITLE = """# PFE proposal A — Predictive maintenance on turbofan sensor data (NASA C-MAPSS)
Baseline: causal rolling features → gradient-boosting RUL regressor (engine-grouped CV) + Isolation-Forest health monitor with k-consecutive-cycle alarms.
Runs on CPU in ~1 min. The optional LSTM cell is marked **[GPU — Colab T4]**.
Data: NASA PCoE C-MAPSS (Saxena et al., 2008), downloaded from the public NASA mirror on AWS."""
PIP = "scikit-learn pandas numpy matplotlib"

CELLS = [
("code", """from pdm import data
from pdm.pipeline import run_baseline
try:
    root = data.download_cmapss('data/cmapss')
    train, test, rul = data.load_cmapss(root, 'FD001')
    SOURCE = 'C-MAPSS FD001'
except Exception as e:  # offline fallback so the notebook still runs end to end
    print('Download failed, using synthetic data:', e)
    train = data.make_synthetic(40, seed=0)
    test, rul = data.truncate_for_test(data.make_synthetic(15, seed=1), seed=2)
    SOURCE = 'synthetic'
print(SOURCE, train.shape, test.shape, len(rul))"""),
("code", """res = run_baseline(train, test, rul)
{k: v for k, v in res.items() if k not in ('predictions', 'sensors_used')}"""),
("code", """import matplotlib.pyplot as plt
p = res['predictions'].sort_values('rul_true')
plt.figure(figsize=(8, 3.5))
plt.plot(p['rul_true'].to_numpy(), label='true RUL (capped 125)')
plt.plot(p['rul_pred'].to_numpy(), '.', label='predicted')
plt.xlabel('test engines (sorted by true RUL)'); plt.ylabel('cycles'); plt.legend(); plt.title(f'{SOURCE} — RUL at last observed cycle')
plt.tight_layout(); plt.show()"""),
("md", """## [GPU — Colab T4] Optional: LSTM sequence model (Zheng et al., 2017 style)
Set `RUN_GPU_CELLS = True` in Colab (Runtime → T4 GPU). On CPU it runs a 1-epoch smoke test only."""),
("code", """RUN_GPU_CELLS = False
import numpy as np
try:
    import torch, torch.nn as nn
except ImportError:
    torch = None
if torch is None:
    print('torch not installed — skip (Colab has it preinstalled)')
else:
    from pdm import features as fe
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    sensors = fe.informative_sensors(train)
    tr = fe.add_rul(train).sort_values(['unit', 'cycle'])
    mu, sd = tr[sensors].mean(), tr[sensors].std() + 1e-8
    W = 30
    def windows(df, with_y=True):
        Xs, ys = [], []
        for _, g in df.groupby('unit'):
            a = ((g[sensors] - mu) / sd).to_numpy(np.float32)
            if len(a) < W: a = np.vstack([np.repeat(a[:1], W - len(a), 0), a])
            if with_y:
                y = g['rul'].to_numpy(np.float32)
                y = np.concatenate([np.repeat(y[:1], max(0, W - len(g))), y])
                for i in range(W, len(a) + 1):
                    Xs.append(a[i - W:i]); ys.append(y[i - 1])
            else:
                Xs.append(a[-W:])
        return np.stack(Xs), (np.array(ys) if with_y else None)
    Xw, yw = windows(tr)
    Xt, _ = windows(test.sort_values(['unit', 'cycle']), with_y=False)
    class LSTMRUL(nn.Module):
        def __init__(self, d):
            super().__init__(); self.lstm = nn.LSTM(d, 64, num_layers=2, batch_first=True, dropout=0.2); self.head = nn.Linear(64, 1)
        def forward(self, x):
            h, _ = self.lstm(x); return self.head(h[:, -1]).squeeze(-1)
    m = LSTMRUL(len(sensors)).to(dev); opt = torch.optim.Adam(m.parameters(), 1e-3)
    epochs = 30 if (RUN_GPU_CELLS and dev == 'cuda') else 1
    ds = torch.utils.data.TensorDataset(torch.from_numpy(Xw), torch.from_numpy(yw))
    dl = torch.utils.data.DataLoader(ds, batch_size=256, shuffle=True)
    for ep in range(epochs):
        m.train()
        for xb, yb in dl:
            opt.zero_grad(); loss = nn.functional.mse_loss(m(xb.to(dev)), yb.to(dev)); loss.backward(); opt.step()
    m.eval()
    with torch.no_grad():
        pred = m(torch.from_numpy(Xt).to(dev)).clamp(min=0).cpu().numpy()
    from pdm.evaluate import rmse
    print(f'LSTM ({epochs} epoch(s), {dev}) test RMSE:', round(rmse(np.minimum(rul, 125), pred), 2))"""),
("md", """## Next steps for the PFE
1. Replace C-MAPSS with the host's sensor/maintenance logs; keep the same `features.py` for training and serving.
2. Add held-out-unit alarm evaluation and a cost model (missed failure vs. false alarm).
3. Calibrate the alarm threshold on business cost, then wrap the model in a FastAPI service + drift monitoring (see proposal C)."""),
]
