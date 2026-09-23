"""FastAPI inference service for the PyTorch MLP example."""
from pathlib import Path

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from model import MLP

PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "model.pth"

app = FastAPI(title="PyTorch MLP API", version="1.0.0")


class InputData(BaseModel):
    x1: float
    x2: float


def load_model() -> MLP:
    """Load the trained model from the project directory."""
    if not MODEL_PATH.is_file():
        raise FileNotFoundError("model.pth not found. Run train.py first.")
    model = MLP()
    state = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
    model.load_state_dict(state)
    model.eval()
    return model


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "MLP API is running"}


@app.post("/predict")
def predict(data: InputData) -> dict[str, float | int]:
    try:
        model = load_model()
    except FileNotFoundError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    X = torch.tensor([[data.x1, data.x2]], dtype=torch.float32)
    with torch.no_grad():
        probability = torch.sigmoid(model(X)).item()

    return {"prediction": int(probability >= 0.5), "probability": probability}
