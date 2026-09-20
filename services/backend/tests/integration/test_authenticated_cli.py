import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_authenticated_cli_api_happy():
    payload = {
        "command": "agentctl logs task-1",
        "format": "json"
    }
    response = client.post("/api/v1/cli/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == "task-1"
    assert data["events"] == []
    assert data["exit_code"] == 0

def test_authenticated_cli_api_missing():
    response = client.post("/api/v1/cli/execute", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
