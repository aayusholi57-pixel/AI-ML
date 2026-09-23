import torch
import torch.nn as nn
import torch.optim as optim

from model import MLP


# -------------------------
# 1. Create random dataset
# -------------------------

torch.manual_seed(42)

X = torch.randn(1000, 2)

y = (X[:, 0] + X[:, 1] > 0).float().unsqueeze(1)


# -------------------------
# 2. Create model
# -------------------------

model = MLP()


# -------------------------
# 3. Loss and optimizer
# -------------------------

loss_function = nn.BCEWithLogitsLoss()

optimizer = optim.Adam(
    model.parameters(),
    lr=0.01
)


# -------------------------
# 4. Training
# -------------------------

for epoch in range(100):

    # Forward
    output = model(X)

    # Loss
    loss = loss_function(output, y)

    # Backward
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(
            f"Epoch: {epoch}, Loss: {loss.item():.4f}"
        )


# -------------------------
# 5. Save model
# -------------------------

torch.save(
    model.state_dict(),
    "model.pth"
)

print("Model saved as model.pth")


# Load the saved weights from disk
model = MLP()

model.load_state_dict(
    torch.load("model.pth", map_location="cpu")
)

model.eval()


