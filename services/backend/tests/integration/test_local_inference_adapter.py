import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_models_local_happy_path():
    payload = {"endpoint": "http://local-model:11434", "privacy_mode": "local_only"}
    response = client.post("/api/v1/models/local", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["provider_id"] == "local-1"
    assert data["external_requests"] == 0

def test_models_local_unavailable():
    payload = {"endpoint": "http://unreachable:11434", "privacy_mode": "local_only"}
    response = client.post("/api/v1/models/local", json=payload)
    assert response.status_code == 503
    data = response.json()
    assert data["error"]["code"] == "SERVICE_UNAVAILABLE"

def test_models_local_missing_field():
    response = client.post("/api/v1/models/local", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
