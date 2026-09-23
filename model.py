"""Minimal sentiment-analysis model example.

The Hugging Face pipeline is created lazily so importing this module does not
download model weights or require network access.
"""

from functools import lru_cache

from transformers import pipeline


@lru_cache(maxsize=1)
def get_classifier():
    """Create and cache the sentiment pipeline on first prediction."""
    return pipeline("sentiment-analysis")


def predict_sentiment(text: str) -> dict[str, float | str]:
    """Predict sentiment for a single non-empty text string."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")

    result = get_classifier()(text.strip(), truncation=True)[0]
    return {
        "label": str(result["label"]),
        "score": float(result["score"]),
    }


if __name__ == "__main__":
    print(predict_sentiment("This is a great learning project"))
