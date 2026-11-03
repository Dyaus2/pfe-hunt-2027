"""Data access for NASA C-MAPSS turbofan run-to-failure data (+ a synthetic stand-in for tests).

Source (public, NASA PCoE repository mirror on AWS):
https://phm-datasets.s3.amazonaws.com/NASA/6.+Turbofan+Engine+Degradation+Simulation+Data+Set.zip
Reference: Saxena et al., 2008, doi:10.1109/PHM.2008.4711414
"""
from __future__ import annotations

import io
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

CMAPSS_URL = "https://phm-datasets.s3.amazonaws.com/NASA/6.+Turbofan+Engine+Degradation+Simulation+Data+Set.zip"
COLUMNS = ["unit", "cycle", "op1", "op2", "op3"] + [f"s{i}" for i in range(1, 22)]


def download_cmapss(dest: str | Path = "data/cmapss", url: str = CMAPSS_URL) -> Path:
    """Download and extract the C-MAPSS text files into `dest` (idempotent)."""
    dest = Path(dest)
    if (dest / "train_FD001.txt").exists():
        return dest
    dest.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as r:
        outer = zipfile.ZipFile(io.BytesIO(r.read()))
    inner_name = next(n for n in outer.namelist() if n.endswith("CMAPSSData.zip"))
    inner = zipfile.ZipFile(io.BytesIO(outer.read(inner_name)))
    for n in inner.namelist():
        if n.endswith(".txt"):
            (dest / Path(n).name).write_bytes(inner.read(n))
    return dest


def _read_txt(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep=r"\s+", header=None)
    df = df.iloc[:, : len(COLUMNS)]
    df.columns = COLUMNS
    df[["unit", "cycle"]] = df[["unit", "cycle"]].astype(int)
    return df


def load_cmapss(root: str | Path, subset: str = "FD001") -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray]:
    """Return (train, test, rul_test). rul_test[i] = true RUL at the last test cycle of unit i+1."""
    root = Path(root)
    train = _read_txt(root / f"train_{subset}.txt")
    test = _read_txt(root / f"test_{subset}.txt")
    rul = pd.read_csv(root / f"RUL_{subset}.txt", sep=r"\s+", header=None).iloc[:, 0].to_numpy()
    return train, test, rul


def make_synthetic(n_units: int = 30, seed: int = 0, min_life: int = 120, max_life: int = 260) -> pd.DataFrame:
    """Run-to-failure data with the C-MAPSS schema: sensors drift exponentially as health degrades.

    Used for unit tests and as an offline fallback; it is NOT a substitute for the real benchmark.
    """
    rng = np.random.default_rng(seed)
    rows = []
    informative = {2: 0.8, 3: 1.0, 4: 1.2, 7: -0.9, 11: 1.1, 12: -0.8, 15: 0.9, 17: 0.7, 20: -0.6, 21: -0.7}
    for u in range(1, n_units + 1):
        life = int(rng.integers(min_life, max_life))
        onset = rng.uniform(0.3, 0.6) * life
        base = rng.normal(0, 1, 21)
        for c in range(1, life + 1):
            deg = np.exp(max(0.0, c - onset) / (life - onset) * 3.0) - 1.0  # 0 → ~19 at failure
            s = base + rng.normal(0, 0.25, 21)
            for k, w in informative.items():
                s[k - 1] += w * deg / 6.0
            s[0] = 518.67  # constant sensor, as s1 in FD001
            rows.append([u, c, rng.normal(0, 0.002), rng.normal(0, 0.0003), 100.0, *s])
    return pd.DataFrame(rows, columns=COLUMNS)


def truncate_for_test(df: pd.DataFrame, seed: int = 0) -> tuple[pd.DataFrame, np.ndarray]:
    """Mimic the C-MAPSS test protocol: cut each unit at a random point, return remaining RUL."""
    rng = np.random.default_rng(seed)
    parts, rul = [], []
    for _, g in df.groupby("unit"):
        life = len(g)
        cut = int(rng.integers(int(0.3 * life), life))
        parts.append(g.iloc[:cut])
        rul.append(life - cut)
    return pd.concat(parts, ignore_index=True), np.array(rul)
