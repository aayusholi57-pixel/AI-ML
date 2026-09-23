"""Execution-level regression tests for the maintained API."""

from fastapi.testclient import TestClient

from servermodel import app


def test_root_and_student_api_contract() -> None:
    client = TestClient(app)
    assert client.get("/").json() == {"message": "AI/ML API is running"}
    response = client.get("/students/42")
    assert response.status_code == 200
    assert response.json() == {"student_id": 42}
