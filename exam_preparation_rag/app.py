"""FastAPI API for the Exam Preparation RAG application."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .rag_engine import DEFAULT_TOP_K, MAX_TOP_K, exam_rag, knowledge_base

app = FastAPI(
    title="Exam Preparation RAG API",
    description="Grounded question answering over local PDF study material.",
    version="2.0.0",
)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    mode: str = Field(default="explain", pattern=r"^(explain|short|5-mark|mcq)$")
    k: int = Field(default=DEFAULT_TOP_K, ge=1, le=MAX_TOP_K)


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"message": "Exam Preparation RAG API is running", "docs": "/docs", "ask": "/ask"}


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready", tags=["system"])
def ready() -> dict[str, int | str]:
    """Verify that the local PDF retrieval index can be built."""
    try:
        chunks, *_ = knowledge_base()
        return {"status": "ready", "chunks": len(chunks)}
    except (FileNotFoundError, ValueError) as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@app.post("/ask", tags=["rag"])
def ask(request: QuestionRequest) -> dict:
    try:
        return exam_rag(request.question, request.mode, request.k)
    except (FileNotFoundError, RuntimeError, ValueError) as error:
        status = 503 if isinstance(error, RuntimeError) else 400
        raise HTTPException(status_code=status, detail=str(error)) from error
