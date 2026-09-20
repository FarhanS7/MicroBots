import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main import app

client = TestClient(app)

def test_policy_happy_path() -> None:
    response = client.post(
        "/api/v1/policy/tool",
        json={"tool": "file.read", "path": "notes.md", "policy_revision": 1},
    )
    assert response.status_code == 200
    assert response.json() == {
        "decision": "allow",
        "policy_revision": 1,
    }

def test_policy_blocked_tool() -> None:
    response = client.post(
        "/api/v1/policy/tool",
        json={"tool": "shell.outbound_write", "path": "/etc/passwd", "policy_revision": 1},
    )
    assert response.status_code == 200
    assert response.json() == {
        "decision": "block",
        "policy_revision": 1,
    }

def test_policy_missing_field() -> None:
    response = client.post("/api/v1/policy/tool", json={})
    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Required input fields are missing",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }
