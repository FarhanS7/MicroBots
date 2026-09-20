import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_runtime_recover_happy_path():
    payload = {"task_id": "task-1", "checkpoint": "after-tool-result"}
    response = client.post("/api/v1/runtime/recover", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["resumed"] is True
    assert data["duplicate_external_effects"] == 0

def test_runtime_recover_unknown_outcome():
    payload = {"task_id": "task-1", "checkpoint": "unknown"}
    response = client.post("/api/v1/runtime/recover", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "OUTCOME_UNKNOWN"

def test_runtime_recover_missing_field():
    response = client.post("/api/v1/runtime/recover", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
