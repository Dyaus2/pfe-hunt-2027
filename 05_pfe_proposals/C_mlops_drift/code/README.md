# MLOps starter kit: drift monitoring + champion/challenger + rollback
PSI drift, quality gates (AUC, ECE, no-regression), file model registry with promote/rollback, prequential simulator of static vs periodic vs champion/challenger.

**Status:** starter skeleton for a PFE pitch, tested on CPU on 2026-11-03 (`pytest` green, notebook executed end to end).
**Measured baseline:** Elec2 (134 weekly batches): mean AUC static 0.764, periodic 0.839, champion/challenger 0.845 (20 promotions, 5 rollbacks).

## Layout
```
src/driftops/{data,drift,gates,registry,loop}.py
tests/            pytest suite (synthetic data, runs offline in seconds)
notebooks/C_mlops_drift_colab.ipynb   self-contained Colab notebook (embeds src/, executed outputs included)
notebooks/cells.py   notebook source; rebuild with: python ../../tools/build_notebook.py ../../C_mlops_drift
requirements.txt
```

## Run
```bash
pip install -r requirements.txt
python -m pytest -q
python -c "import sys,tempfile; sys.path.insert(0,'src'); from driftops import data; from driftops.loop import *; X,y=data.load_electricity(); B=list(data.batches(X,y)); print(summarize(run_stream(B, LoopConfig(), tempfile.mkdtemp())))"
```
**Colab:** upload `notebooks/C_mlops_drift_colab.ipynb` (File → Upload notebook) and *Run all*; it writes the package itself, no clone needed. Cells marked **[GPU — Colab T4]** need Runtime → Change runtime type → T4 GPU (they also run as a slow CPU smoke test).

## My role
Designed and implemented by Hazem Ilahi as a PFE proposal starter; see `../pitch_EN.md`, `../pitch_FR.md`, `../literature.md`.
