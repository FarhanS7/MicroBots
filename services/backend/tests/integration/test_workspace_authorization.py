import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main import app

client = TestClient(app)

def test_workspace_happy_path() -> None:
    response = client.post(
        "/api/v1/workspace/authorize",
        json={"resource_workspace_id": "ws-1"},
        headers={"X-Actor-Workspace-ID": "ws-1"},
    )
    assert response.status_code == 200
    assert response.json() == {"authorized": True}

def test_workspace_cross_tenant_not_found() -> None:
    response = client.post(
        "/api/v1/workspace/authorize",
        json={"resource_workspace_id": "ws-1"},
        headers={"X-Actor-Workspace-ID": "ws-2"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "NOT_FOUND",
            "message": "Resource not found or access denied",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }

def test_workspace_missing_field() -> None:
    response = client.post("/api/v1/workspace/authorize", json={})
    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Required input fields are missing",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }
