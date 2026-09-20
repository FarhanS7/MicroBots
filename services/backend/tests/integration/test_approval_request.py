import pytest
from fastapi.testclient import TestClient
from main import app
from oap.policy.approval_request import reset_approval_store

client = TestClient(app)

def setup_function():
    reset_approval_store()

def test_policy_approval_happy_path():
    payload = {
        "task_id": "task-1",
        "action": "external.publish",
        "target": "fixture-post",
        "expires_in_seconds": 3600,
    }
    response = client.post("/api/v1/policy/approval", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["approval_id"] == "approval-1"
    assert data["state"] == "pending"

def test_policy_approval_invalid():
    payload = {
        "task_id": "task-1",
        "action": "external.publish",
        "target": "fixture-post",
        "expires_in_seconds": 0,
    }
    response = client.post("/api/v1/policy/approval", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "Invalid approval request parameters" in data["error"]["message"]

def test_policy_approval_missing_field():
    response = client.post("/api/v1/policy/approval", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
