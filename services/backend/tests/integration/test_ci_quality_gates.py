import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main import app

client = TestClient(app)

def test_ci_happy_path() -> None:
    response = client.post("/api/v1/ci/verify", json={"event": "pull_request", "fork": True})
    assert response.status_code == 200
    assert response.json() == {
        "checks_required": True,
        "secrets_available": False,
    }

def test_ci_non_fork() -> None:
    response = client.post("/api/v1/ci/verify", json={"event": "push", "fork": False})
    assert response.status_code == 200
    assert response.json() == {
        "checks_required": True,
        "secrets_available": True,
    }

def test_ci_missing_field() -> None:
    response = client.post("/api/v1/ci/verify", json={})
    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Required input fields are missing",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }
