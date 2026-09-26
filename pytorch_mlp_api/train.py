"""Train and persist the small PyTorch MLP used by the API."""
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim

from model import MLP

PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "model.pth"


def make_dataset(n_samples: int = 1000):
    """Create a deterministic two-feature classification dataset."""
    generator = torch.Generator().manual_seed(42)
    X = torch.randn(n_samples, 2, generator=generator)
    y = (X[:, 0] + X[:, 1] > 0).float().unsqueeze(1)
    return X, y


def train(epochs: int = 100) -> tuple[MLP, float]:
    """Train the MLP and return the model plus final loss."""
    X, y = make_dataset()
    model = MLP()
    loss_function = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    for epoch in range(epochs):
        output = model(X)
        loss = loss_function(output, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if epoch % 10 == 0:
            print(f"Epoch: {epoch}, Loss: {loss.item():.4f}")

    return model, float(loss.item())


def save_model(model: MLP) -> None:
    """Save model weights beside this script."""
    torch.save(model.state_dict(), MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    trained_model, final_loss = train()
    save_model(trained_model)
    print(f"Final loss: {final_loss:.4f}")
