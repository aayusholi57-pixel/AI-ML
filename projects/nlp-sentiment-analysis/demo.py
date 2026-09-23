"""CLI demo for the NLP sentiment project."""

from sentiment import predict, train_full_model


def main() -> None:
    model = train_full_model()
    print("NLP Sentiment Demo")
    print("Type a sentence, or press Ctrl+C to exit.")
    while True:
        text = input("> ").strip()
        if not text:
            continue
        label, confidence = predict(model, text)
        print(f"sentiment={label} confidence={confidence:.3f}")


if __name__ == "__main__":
    main()
