import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_web_approval_happy_path():
    payload = {"approval_id": "approval-1", "decision": "deny"}
    response = client.post("/api/v1/web/approval", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["visible_state"] == "denied"
    assert data["action_executed"] is False

def test_web_approval_expired():
    payload = {"approval_id": "expired", "decision": "deny"}
    response = client.post("/api/v1/web/approval", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "EXPIRED"

def test_web_approval_missing_field():
    response = client.post("/api/v1/web/approval", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
