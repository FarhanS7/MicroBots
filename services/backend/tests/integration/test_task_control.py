import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_tasks_control_happy_path():
    payload = {"task_id": "task-1", "action": "cancel", "expected_revision": 2}
    response = client.post("/api/v1/tasks/control", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == "task-1"
    assert data["cancellation_requested"] is True

def test_tasks_control_conflict():
    payload = {"task_id": "task-1", "action": "cancel", "expected_revision": 0}
    response = client.post("/api/v1/tasks/control", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_tasks_control_missing_field():
    response = client.post("/api/v1/tasks/control", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
