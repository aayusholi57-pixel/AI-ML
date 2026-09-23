from fastapi.testclient import TestClient

from servermodel import app

client = TestClient(app)


def test_root_health() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "AI/ML API is running"


def test_student_endpoint() -> None:
    response = client.get("/students/42")
    assert response.status_code == 200
    assert response.json() == {"student_id": 42}
