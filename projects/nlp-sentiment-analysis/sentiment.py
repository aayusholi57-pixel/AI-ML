"""Reproducible sentiment baseline and inference helpers.

TF-IDF + LogisticRegression provides a deterministic offline baseline that can
be evaluated in CI. The repository's Transformer example remains separate.
"""

from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.pipeline import Pipeline


@dataclass(frozen=True)
class EvaluationResult:
    accuracy: float
    precision: float
    recall: float
    f1: float


DATASET = (
    ("I love this excellent product", "positive"),
    ("This is a great and helpful product", "positive"),
    ("The service was excellent and wonderful", "positive"),
    ("I am very happy with this result", "positive"),
    ("Amazing quality and great service", "positive"),
    ("I would recommend this excellent service", "positive"),
    ("The support team was wonderful and helpful", "positive"),
    ("This product is good and reliable", "positive"),
    ("I hate this terrible product", "negative"),
    ("This is a bad and useless product", "negative"),
    ("The service was terrible and awful", "negative"),
    ("I am very unhappy with this result", "negative"),
    ("Poor quality and bad service", "negative"),
    ("I would not recommend this terrible service", "negative"),
    ("The support team was horrible and unhelpful", "negative"),
    ("This product is bad and unreliable", "negative"),
)


def build_model() -> Pipeline:
    """Build the reproducible TF-IDF + logistic-regression baseline."""
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), lowercase=True)),
        ("classifier", LogisticRegression(random_state=42, max_iter=1000)),
    ])


def evaluate(model: Pipeline, texts: list[str], labels: list[str]) -> EvaluationResult:
    """Evaluate a fitted classifier on held-out examples."""
    predictions = model.predict(texts)
    return EvaluationResult(
        accuracy=accuracy_score(labels, predictions),
        precision=precision_score(labels, predictions, pos_label="positive", zero_division=0),
        recall=recall_score(labels, predictions, pos_label="positive", zero_division=0),
        f1=f1_score(labels, predictions, pos_label="positive", zero_division=0),
    )


def train_and_evaluate() -> EvaluationResult:
    """Train on a fixed, class-balanced holdout split and return metrics."""
    train_data = DATASET[:6] + DATASET[8:14]
    test_data = DATASET[6:8] + DATASET[14:16]
    train_texts, train_labels = zip(*train_data)
    test_texts, test_labels = zip(*test_data)
    model = build_model().fit(train_texts, train_labels)
    return evaluate(model, list(test_texts), list(test_labels))


def train_full_model() -> Pipeline:
    """Fit the demo model on the complete educational dataset."""
    texts, labels = zip(*DATASET)
    return build_model().fit(texts, labels)


def predict(model: Pipeline, text: str) -> tuple[str, float]:
    """Predict a sentiment label and class probability."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")
    probabilities = model.predict_proba([text.strip()])[0]
    index = int(probabilities.argmax())
    return str(model.classes_[index]), float(probabilities[index])


if __name__ == "__main__":
    result = train_and_evaluate()
    print(f"accuracy={result.accuracy:.3f}")
    print(f"precision={result.precision:.3f}")
    print(f"recall={result.recall:.3f}")
    print(f"f1={result.f1:.3f}")
