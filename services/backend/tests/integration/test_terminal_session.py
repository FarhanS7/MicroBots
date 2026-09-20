import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_terminal_happy_path():
    payload = {
        "command": "printf hello",
        "cwd": "/workspace",
        "timeout_seconds": 5,
    }
    response = client.post("/api/v1/execution/terminal", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["stdout"] == "hello"
    assert data["stderr"] == ""
    assert data["exit_code"] == 0

def test_terminal_deadline_exceeded():
    payload = {
        "command": "sleep 10",
        "cwd": "/workspace",
        "timeout_seconds": 0,
    }
    response = client.post("/api/v1/execution/terminal", json=payload)
    assert response.status_code == 504
    data = response.json()
    assert data["error"]["code"] == "DEADLINE_EXCEEDED"
    assert "Process execution exceeded timeout limit" in data["error"]["message"]

def test_terminal_missing_field():
    response = client.post("/api/v1/execution/terminal", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
