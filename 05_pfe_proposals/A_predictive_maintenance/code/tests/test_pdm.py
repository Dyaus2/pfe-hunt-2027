import numpy as np
import pandas as pd
import pytest

from pdm import data, evaluate, features
from pdm.pipeline import run_baseline


@pytest.fixture(scope="module")
def synth():
    full = data.make_synthetic(n_units=24, seed=1)
    test_full = data.make_synthetic(n_units=10, seed=2)
    test, rul = data.truncate_for_test(test_full, seed=3)
    return full, test, rul


def test_schema(synth):
    full, _, _ = synth
    assert list(full.columns) == data.COLUMNS
    assert full.groupby("unit")["cycle"].apply(lambda c: (np.diff(c) == 1).all()).all()


def test_rul_target_is_capped_and_ends_at_zero(synth):
    full, _, _ = synth
    t = features.add_rul(full, cap=125)
    assert t["rul"].max() <= 125
    assert (t.groupby("unit")["rul"].min() == 0).all()


def test_constant_sensor_dropped(synth):
    full, _, _ = synth
    assert "s1" not in features.informative_sensors(full)


def test_rolling_features_are_causal(synth):
    full, _, _ = synth
    sensors = features.informative_sensors(full)
    X1 = features.rolling_features(full, sensors)
    # changing a FUTURE value must not change features at an earlier cycle
    mod = full.copy()
    mask = (mod["unit"] == 1) & (mod["cycle"] == 50)
    mod.loc[mask, sensors[0]] += 100.0
    X2 = features.rolling_features(mod, sensors)
    early = (X1["unit"] == 1) & (X1["cycle"] < 50)
    pd.testing.assert_frame_equal(X1[early], X2[early])


def test_phm08_penalises_late_more_than_early():
    assert evaluate.phm08_score([50], [60]) > evaluate.phm08_score([50], [40])
    assert evaluate.phm08_score([10, 20], [10, 20]) == 0.0


def test_pipeline_end_to_end(synth):
    full, test, rul = synth
    res = run_baseline(full, test, rul, n_splits=4)
    assert np.isfinite(res["test_rmse"]) and res["test_rmse"] < 60  # far better than predicting a constant
    assert 0.0 <= res["alarms_on_train_units"]["detection_rate"] <= 1.0
    assert len(res["predictions"]) == test["unit"].nunique()
    assert (res["predictions"]["rul_pred"] >= 0).all()
