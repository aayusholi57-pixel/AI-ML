"""Execution-level regression tests for the maintained API."""

from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from servermodel import app  # noqa: E402


def test_root_and_student_api_contract() -> None:
    client = TestClient(app)
    assert client.get("/").json() == {"message": "AI/ML API is running"}
    response = client.get("/students/42")
    assert response.status_code == 200
    assert response.json() == {"student_id": 42}
