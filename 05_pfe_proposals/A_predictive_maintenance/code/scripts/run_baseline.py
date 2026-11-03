"""CLI: python scripts/run_baseline.py --source cmapss|synthetic [--subset FD001]"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pdm import data  # noqa: E402
from pdm.pipeline import run_baseline  # noqa: E402

p = argparse.ArgumentParser()
p.add_argument("--source", choices=["cmapss", "synthetic"], default="cmapss")
p.add_argument("--subset", default="FD001")
p.add_argument("--data-dir", default="data/cmapss")
a = p.parse_args()

if a.source == "cmapss":
    root = data.download_cmapss(a.data_dir)
    train, test, rul = data.load_cmapss(root, a.subset)
else:
    train = data.make_synthetic(40, seed=0)
    test, rul = data.truncate_for_test(data.make_synthetic(15, seed=1), seed=2)

res = run_baseline(train, test, rul)
print(json.dumps({k: v for k, v in res.items() if k != "predictions"}, indent=2))
