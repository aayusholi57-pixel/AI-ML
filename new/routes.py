from fastapi import FastAPI
from model import predict_sentiment
app = FastAPI()

@app.get("/model/{user_review}")
def get_model(user_review: str):
    verdict = predict_sentiment(user_review)
    return {"verdict": verdict}
