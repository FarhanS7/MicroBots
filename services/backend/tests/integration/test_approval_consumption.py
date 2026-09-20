import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_policy_consume_happy_path():
    payload = {
        "approval_id": "approval-1",
        "decision": "approve_once",
        "expected_revision": 1,
    }
    response = client.post("/api/v1/policy/consume", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["state"] == "approved"
    assert data["revision"] == 2

def test_policy_consume_conflict():
    payload = {
        "approval_id": "approval-1",
        "decision": "approve_once",
        "expected_revision": 0,
    }
    response = client.post("/api/v1/policy/consume", json=payload)
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "REVISION_CONFLICT"

def test_policy_consume_missing_field():
    response = client.post("/api/v1/policy/consume", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
