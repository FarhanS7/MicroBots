import pytest
from fastapi.testclient import TestClient
from main import app
from oap.execution.sandbox_broker import reset_computers_store

client = TestClient(app)

def setup_function():
    reset_computers_store()

def test_sandbox_happy_path():
    payload = {
        "task_id": "task-1",
        "workspace_id": "ws-1",
        "image": "fixture-pinned-image",
    }
    response = client.post("/api/v1/execution/sandbox", json=payload, headers={"X-Actor-Workspace-ID": "ws-1"})
    assert response.status_code == 200
    data = response.json()
    assert data["computer_id"] == "computer-1"
    assert data["state"] == "ready"

def test_sandbox_forbidden_grant():
    payload = {
        "task_id": "task-1",
        "workspace_id": "ws-1",
        "image": "fixture-pinned-image",
    }
    response = client.post("/api/v1/execution/sandbox", json=payload, headers={"X-Actor-Workspace-ID": "ws-other"})
    assert response.status_code == 403
    data = response.json()
    assert data["error"]["code"] == "FORBIDDEN"
    assert "Invalid or expired workspace grant" in data["error"]["message"]

def test_sandbox_missing_field():
    response = client.post("/api/v1/execution/sandbox", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
