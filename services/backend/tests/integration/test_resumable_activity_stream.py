import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_events_stream_happy_path():
    payload = {"after": 4, "workspace_id": "ws-1"}
    response = client.post("/api/v1/events/stream", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["sequences"] == [5, 6]
    assert data["next_cursor"] == 6

def test_events_stream_resync_required():
    payload = {"after": 0, "workspace_id": "ws-resync"}
    response = client.post("/api/v1/events/stream", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "RESYNC_REQUIRED"
    assert "Cursor older than retention window requires resync" in data["error"]["message"]

def test_events_stream_missing_field():
    response = client.post("/api/v1/events/stream", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
