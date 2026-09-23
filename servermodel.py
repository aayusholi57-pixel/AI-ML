"""Minimal FastAPI example for serving an ML-related API.

Run:
    uvicorn servermodel:app --reload
"""

from fastapi import FastAPI

app = FastAPI(
    title="AI/ML Learning API",
    version="1.0.0",
    description="Small, documented API examples from the AI/ML engineering workspace.",
)


@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    """Return a simple health response."""
    return {"message": "AI/ML API is running"}


@app.get("/students/{student_id}", tags=["students"])
def get_student(student_id: int) -> dict[str, int]:
    """Return the supplied student identifier."""
    return {"student_id": student_id}
