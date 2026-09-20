import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_runtime_happy_path():
    payload = {"task_id": "task-1", "max_steps": 10}
    response = client.post("/api/v1/runtime/loop", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == "task-1"
    assert data["state"] == "completed"
    assert data["artifact_ids"] == ["artifact-1"]

def test_runtime_budget_exceeded():
    payload = {"task_id": "task-1", "max_steps": 0}
    response = client.post("/api/v1/runtime/loop", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "BUDGET_EXCEEDED"
    assert "Execution budget exceeded max steps limit" in data["error"]["message"]

def test_runtime_missing_field():
    response = client.post("/api/v1/runtime/loop", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
