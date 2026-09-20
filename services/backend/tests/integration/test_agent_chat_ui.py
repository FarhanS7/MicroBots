import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_web_chat_happy_path():
    payload = {"agent_id": "agent-1", "instruction": "Research three competitors"}
    response = client.post("/api/v1/web/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["visible_task_id"] == "task-1"
    assert data["visible_state"] == "queued"

def test_web_chat_submission_error():
    payload = {"agent_id": "agent-1", "instruction": "fail"}
    response = client.post("/api/v1/web/chat", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "SUBMISSION_ERROR"

def test_web_chat_missing_field():
    response = client.post("/api/v1/web/chat", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
