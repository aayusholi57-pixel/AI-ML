"""Execution tests for the breast-cancer classification benchmark."""

import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))

from train import FEATURES, build_model, load_data, train_and_evaluate  # noqa: E402


def test_dataset_contract() -> None:
    X, y = load_data()
    assert list(X.columns) == FEATURES
    assert len(X) == 569
    assert set(y.unique()) == {0, 1}


def test_model_evaluation_metrics_are_real_and_bounded() -> None:
    model, metrics = train_and_evaluate()
    assert model is not None
    for value in (metrics.accuracy, metrics.precision, metrics.recall, metrics.f1):
        assert 0.0 <= value <= 1.0
    assert metrics.test_size == 114
    assert metrics.f1 >= 0.85


def test_model_can_predict_known_row() -> None:
    X, _ = load_data()
    model, _ = train_and_evaluate()
    prediction = model.predict(X.iloc[[0]])[0]
    assert prediction in {0, 1}


def test_pipeline_has_scaling_before_classifier() -> None:
    model = build_model()
    assert list(model.named_steps) == ["scaler", "classifier"]
