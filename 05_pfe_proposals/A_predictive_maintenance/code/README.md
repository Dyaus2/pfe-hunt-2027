# Predictive maintenance starter kit (NASA C-MAPSS)
RUL regression (gradient boosting, engine-grouped CV, PHM08 score) + Isolation-Forest health monitor with k-consecutive-cycle alarms.

**Status:** starter skeleton for a PFE pitch, tested on CPU on 2026-11-03 (`pytest` green, notebook executed end to end).
**Measured baseline:** FD001: test RMSE 15.3, CV RMSE 18.7 ± 0.7, PHM08 score 382; alarm diagnostics on training engines: detection 100%, median lead time 41.5 cycles.

## Layout
```
src/pdm/{data,features,models,evaluate,pipeline}.py
tests/            pytest suite (synthetic data, runs offline in seconds)
notebooks/A_predictive_maintenance_colab.ipynb   self-contained Colab notebook (embeds src/, executed outputs included)
notebooks/cells.py   notebook source; rebuild with: python ../../tools/build_notebook.py ../../A_predictive_maintenance
requirements.txt
```

## Run
```bash
pip install -r requirements.txt
python -m pytest -q
python scripts/run_baseline.py --source cmapss   # downloads NASA C-MAPSS (~12 MB)
python scripts/run_baseline.py --source synthetic  # offline
```
**Colab:** upload `notebooks/A_predictive_maintenance_colab.ipynb` (File → Upload notebook) and *Run all*; it writes the package itself, no clone needed. Cells marked **[GPU — Colab T4]** need Runtime → Change runtime type → T4 GPU (they also run as a slow CPU smoke test).

## My role
Designed and implemented by Hazem Ilahi as a PFE proposal starter; see `../pitch_EN.md`, `../pitch_FR.md`, `../literature.md`.
