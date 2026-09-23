"""Minimal sentiment-analysis model example.

The Hugging Face pipeline downloads the model on first use.
"""

from transformers import pipeline

classifier = pipeline("sentiment-analysis")


def predict_sentiment(text: str) -> dict:
    """Predict sentiment for a single piece of text."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")

    result = classifier(text.strip(), truncation=True)[0]
    return {
        "label": result["label"],
        "score": float(result["score"]),
    }


if __name__ == "__main__":
    print(predict_sentiment("This is a great learning project"))
