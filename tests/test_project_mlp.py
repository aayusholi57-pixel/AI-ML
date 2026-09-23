"""Execution tests for the PyTorch MLP project."""

import sys
from pathlib import Path

import torch
from fastapi.testclient import TestClient

PROJECT_DIR = Path(__file__).resolve().parents[1] / "new1"
sys.path.insert(0, str(PROJECT_DIR))

from main import app  # noqa: E402
from train import make_dataset, train  # noqa: E402


def test_training_path_reduces_loss() -> None:
    torch.manual_seed(42)
    _, final_loss = train(epochs=30)
    assert final_loss < 0.20


def test_dataset_is_deterministic() -> None:
    first = make_dataset(32)
    second = make_dataset(32)
    assert torch.equal(first[0], second[0])
    assert torch.equal(first[1], second[1])


def test_api_contract() -> None:
    client = TestClient(app)
    response = client.post("/predict", json={"x1": 1.0, "x2": -1.0})
    assert response.status_code in {200, 503}
    if response.status_code == 200:
        body = response.json()
        assert body["prediction"] in {0, 1}
        assert 0.0 <= body["probability"] <= 1.0
