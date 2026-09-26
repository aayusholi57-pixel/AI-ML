"""Small PyTorch multilayer perceptron used by the MLP API."""

import torch
from torch import nn


class MLP(nn.Module):
    """Two-layer MLP for the synthetic two-feature classification task."""

    def __init__(self) -> None:
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(2, 10),
            nn.ReLU(),
            nn.Linear(10, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Return the raw classification logit."""
        return self.layers(x)
