import pytest
from fastapi.testclient import TestClient
from main import app
from oap.memory.memory_governance import reset_memory_store

client = TestClient(app)

def setup_function():
    reset_memory_store()

def test_memory_govern_happy_path():
    payload = {"category": "preference", "text": "Use concise summaries", "source_message_id": "message-1"}
    response = client.post("/api/v1/memory/govern", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["memory_id"] == "memory-1"
    assert data["status"] == "user_confirmed"

def test_memory_govern_disabled():
    payload = {"category": "preference", "text": "Use concise summaries", "source_message_id": "disabled"}
    response = client.post("/api/v1/memory/govern", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "MEMORY_DISABLED"

def test_memory_govern_missing_field():
    response = client.post("/api/v1/memory/govern", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
