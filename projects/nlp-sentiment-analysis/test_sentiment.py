"""Execution and evaluation tests for the NLP sentiment project."""

import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))

from sentiment import build_model, evaluate, train_and_evaluate, train_full_model  # noqa: E402


def test_training_produces_real_metrics() -> None:
    result = train_and_evaluate()
    for metric in (result.accuracy, result.precision, result.recall, result.f1):
        assert 0.0 <= metric <= 1.0
    assert result.accuracy >= 0.75
    assert result.f1 >= 0.75


def test_model_can_infer_after_training() -> None:
    model = train_full_model()
    prediction = model.predict(["I love the excellent service"])[0]
    assert prediction == "positive"


def test_metric_function_matches_perfect_predictions() -> None:
    model = build_model().fit(["good", "bad"], ["positive", "negative"])
    result = evaluate(model, ["good", "bad"], ["positive", "negative"])
    assert result.accuracy == 1.0
    assert result.f1 == 1.0
