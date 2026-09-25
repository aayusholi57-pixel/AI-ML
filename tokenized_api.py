from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Header, Depends, HTTPException
import os





class PredictRequest(BaseModel):
    user_query: str


API_KEY = os.environ.get("DAY47_API_KEY", "saarathi-demo-key-123")

app = FastAPI()

def require_api_key(x_api_key: str = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="missing or invalid API key")
    return x_api_key

@app.post("/predict", dependencies=[Depends(require_api_key)])
def predict(req: PredictRequest):
    return {"verdict":"positive"}
