"""Reproducible breast-cancer classification benchmark.

Uses the repository's data.csv and a leakage-safe preprocessing pipeline.
This is an educational benchmark, not a medical diagnostic system.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data.csv"
FEATURES = [
    "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean",
    "compactness_mean", "concavity_mean", "concave points_mean", "symmetry_mean",
    "fractal_dimension_mean", "radius_se", "texture_se", "perimeter_se", "area_se",
    "smoothness_se", "compactness_se", "concavity_se", "concave points_se",
    "symmetry_se", "fractal_dimension_se", "radius_worst", "texture_worst",
    "perimeter_worst", "area_worst", "smoothness_worst", "compactness_worst",
    "concavity_worst", "concave points_worst", "symmetry_worst",
    "fractal_dimension_worst",
]


@dataclass(frozen=True)
class Metrics:
    accuracy: float
    precision: float
    recall: float
    f1: float
    test_size: int


def load_data(path: Path = DATA_PATH) -> tuple[pd.DataFrame, pd.Series]:
    """Load and validate the UCI-style CSV used by the original notebook."""
    if not path.is_file():
        raise FileNotFoundError(f"Dataset not found: {path}")
    df = pd.read_csv(path)
    missing = [column for column in FEATURES + ["diagnosis"] if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    clean = df[FEATURES + ["diagnosis"]].copy()
    clean["diagnosis"] = clean["diagnosis"].astype(str).str.strip().map({"M": 1, "B": 0})
    if clean["diagnosis"].isna().any():
        raise ValueError("diagnosis must contain only M or B")
    return clean[FEATURES], clean["diagnosis"].astype(int)


def build_model() -> Pipeline:
    """Build a leakage-safe standardized logistic-regression pipeline."""
    return Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=5000, random_state=42)),
    ])


def train_and_evaluate() -> tuple[Pipeline, Metrics]:
    """Train on 80% of the data and evaluate on a stratified holdout."""
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    model = build_model().fit(X_train, y_train)
    predictions = model.predict(X_test)
    metrics = Metrics(
        accuracy=accuracy_score(y_test, predictions),
        precision=precision_score(y_test, predictions, zero_division=0),
        recall=recall_score(y_test, predictions, zero_division=0),
        f1=f1_score(y_test, predictions, zero_division=0),
        test_size=len(y_test),
    )
    return model, metrics


if __name__ == "__main__":
    _, metrics = train_and_evaluate()
    for name, value in asdict(metrics).items():
        print(f"{name}={value:.4f}" if isinstance(value, float) else f"{name}={value}")
