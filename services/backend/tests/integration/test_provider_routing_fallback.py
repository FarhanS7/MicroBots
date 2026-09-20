import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_models_route_happy_path():
    payload = {
        "preferred": "provider-1",
        "fallbacks": ["provider-2"],
        "privacy_mode": "external_allowed",
    }
    response = client.post("/api/v1/models/route", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["selected"] == "provider-2"
    assert data["reason"] == "preferred-unavailable"

def test_models_route_unavailable():
    payload = {
        "preferred": "unavailable",
        "fallbacks": [],
        "privacy_mode": "external_allowed",
    }
    response = client.post("/api/v1/models/route", json=payload)
    assert response.status_code == 503
    data = response.json()
    assert data["error"]["code"] == "PROVIDER_UNAVAILABLE"

def test_models_route_missing_field():
    response = client.post("/api/v1/models/route", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
