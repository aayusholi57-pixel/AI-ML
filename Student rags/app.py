"""FastAPI interface for the Exam Preparation RAG project."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .rag_engine import exam_rag

app = FastAPI(title="Exam Preparation RAG API", version="1.0.0")


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1)
    mode: str = Field(default="explain", pattern="^(explain|short|5-mark|mcq)$")
    k: int = Field(default=3, ge=1, le=10)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Exam Preparation RAG API is running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask")
def ask(request: QuestionRequest) -> dict:
    try:
        return exam_rag(request.question, request.mode, request.k)
    except (FileNotFoundError, RuntimeError, ValueError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
