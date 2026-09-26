"""Execution tests for the Dal Bhat computer-vision training path."""

import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))

from PIL import Image

from train import CLASS_NAMES, DATASET_ROOT, predict, train_model


def test_dataset_contract() -> None:
    assert DATASET_ROOT.is_dir()
    folders = sorted(path.name for path in DATASET_ROOT.iterdir() if path.is_dir())
    assert folders == sorted(CLASS_NAMES)


def test_one_epoch_training_and_inference() -> None:
    model, accuracy = train_model(epochs=1)
    assert 0.0 <= accuracy <= 1.0
    label, confidence = predict(model, Image.new("RGB", (224, 224), "white"))
    assert label in {"dalbhat", "not_dalbhat", "uncertain"}
    assert 0.0 <= confidence <= 1.0
