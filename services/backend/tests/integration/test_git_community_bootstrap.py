import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main import app

client = TestClient(app)

def test_bootstrap_happy_path() -> None:
    response = client.post("/api/v1/bootstrap/verify", json={"repository": "open-agent-platform", "visibility": "public"})
    assert response.status_code == 200
    res_data = response.json()
    assert sorted(res_data["branches"]) == ["dev", "main"]
    assert res_data["license"] == "MIT"

def test_bootstrap_missing_field() -> None:
    response = client.post("/api/v1/bootstrap/verify", json={})
    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Required input fields are missing",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }
