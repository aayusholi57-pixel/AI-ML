# PyTorch MLP Classification API

A compact end-to-end neural-network example: generate a reproducible two-feature dataset, train a PyTorch MLP, save its weights, and expose inference through FastAPI.

## Flow

`train.py` → `model.pth` → `main.py` → `POST /predict`

The generated model file is intentionally ignored by Git. Train locally before starting the API.

## Run

```bash
python train.py
uvicorn main:app --reload
```

Open `/docs` to test the API interactively.

## Input

```json
{"x1": 0.4, "x2": -0.2}
```

The example predicts the synthetic decision boundary `x1 + x2 > 0`. It is a learning project, not a real-world predictive model.
