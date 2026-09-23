import torch
from fastapi import FastAPI
from pydantic import BaseModel

from model import MLP


app = FastAPI()


# -------------------------
# Load trained model
# -------------------------

model = MLP()

model.load_state_dict(
    torch.load(
        "model.pth",
        map_location="cpu"
    )
)

model.eval()


# -------------------------
# Request format
# -------------------------

class InputData(BaseModel):
    x1: float
    x2: float


# -------------------------
# Home endpoint
# -------------------------

@app.get("/")
def home():

    return {
        "message": "MLP API is running"
    }


# -------------------------
# Prediction endpoint
# -------------------------

@app.post("/predict")
def predict(data: InputData):

    # Create tensor
    X = torch.tensor([
        [data.x1, data.x2]
    ])


    # Prediction
    with torch.no_grad():

        output = model(X)

        probability = torch.sigmoid(output)

        prediction = (
            probability >= 0.5
        ).int()


    return {
        "prediction": prediction.item(),
        "probability": probability.item()
    }