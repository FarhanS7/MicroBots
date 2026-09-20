import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_memory_retrieve_happy_path():
    payload = {"query": "summary style", "limit": 3}
    response = client.post("/api/v1/memory/retrieve", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["memory_ids"] == ["memory-1"]
    assert data["truncated"] is False

def test_memory_retrieve_error():
    payload = {"query": "invalid", "limit": 3}
    response = client.post("/api/v1/memory/retrieve", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_memory_retrieve_missing_field():
    response = client.post("/api/v1/memory/retrieve", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
