"""CLI demo for the breast-cancer classification benchmark."""

from train import train_and_evaluate


def main() -> None:
    _, metrics = train_and_evaluate()
    print("Breast Cancer Classification Demo")
    print("Held-out evaluation completed")
    print(f"accuracy={metrics.accuracy:.3f}")
    print(f"precision={metrics.precision:.3f}")
    print(f"recall={metrics.recall:.3f}")
    print(f"f1={metrics.f1:.3f}")
    print("Educational benchmark only; not a medical diagnostic tool.")


if __name__ == "__main__":
    main()
