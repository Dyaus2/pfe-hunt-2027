import numpy as np
import pandas as pd
import pytest

from driftops import data
from driftops.drift import drift_flag, feature_psi, psi
from driftops.gates import QualityGates, ece
from driftops.loop import LoopConfig, run_stream, summarize
from driftops.registry import ModelRegistry


def test_psi_stable_vs_shifted():
    rng = np.random.default_rng(0)
    a, b = rng.normal(0, 1, 5000), rng.normal(0, 1, 5000)
    assert psi(a, b) < 0.02
    assert psi(a, b + 1.0) > 0.2
    assert psi(np.ones(100), np.ones(100)) < 1e-6  # constant feature handled


def test_drift_flag():
    assert drift_flag({"a": 0.05, "b": 0.3}, 0.2) and not drift_flag({"a": 0.05}, 0.2)


def test_ece_perfect_and_bad():
    y = np.array([0, 1] * 50)
    assert ece(y, y.astype(float)) == pytest.approx(0.0)
    assert ece(y, np.full(100, 0.9)) == pytest.approx(0.4)


def test_gates():
    y = np.array([0, 1] * 150)
    ok, _ = QualityGates().check(y, np.where(y == 1, 0.95, 0.05))  # ECE 0.05
    miscal, r2 = QualityGates().check(y, np.where(y == 1, 0.8, 0.2))  # ECE 0.2 > 0.15
    assert not miscal and any("ECE" in r for r in r2)
    bad, reasons = QualityGates().check(y, np.full(300, 0.5))
    assert ok and not bad and any("AUC" in r for r in reasons)


def test_registry_promote_rollback(tmp_path):
    r = ModelRegistry(tmp_path)
    v1 = r.register({"m": 1}, {}); r.promote(v1)
    v2 = r.register({"m": 2}, {}); r.promote(v2)
    assert r.rollback("test") == v1 and r.champion == v1 and r.load(v1) == {"m": 1}
    assert ModelRegistry(tmp_path).champion == v1  # persisted


@pytest.fixture(scope="module")
def stream():
    X, y = data.make_synthetic_stream(n_batches=36, size=300, drift_at=16, seed=3)
    return list(data.batches(X, y, size=300))


def test_champion_challenger_recovers_after_abrupt_drift(stream, tmp_path_factory):
    static = run_stream(stream, LoopConfig(strategy="static", window=6), str(tmp_path_factory.mktemp("s")))
    cc = run_stream(stream, LoopConfig(strategy="champion_challenger", window=6), str(tmp_path_factory.mktemp("c")))
    per = run_stream(stream, LoopConfig(strategy="periodic", window=6, period=3), str(tmp_path_factory.mktemp("p")))
    late = lambda log: log[log["batch"] >= 26]["auc"].mean()
    assert summarize(static)["retrains"] == 0
    assert late(cc) > late(static) + 0.2       # static model is stuck on the old concept
    assert summarize(cc)["promotions"] >= 1 and summarize(per)["promotions"] >= 1
    assert cc.loc[cc["batch"] >= 16, "drift"].any()  # PSI sees the covariate shift
