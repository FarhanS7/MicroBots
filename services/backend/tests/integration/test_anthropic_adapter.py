import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from oap.api.models_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_anthropic_adapter_api_happy_path():
    response = client.post(
        "/api/v1/models/anthropic",
        json={"provider": "anthropic", "required_capabilities": ["tools"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["conformance_passed"] is True
    assert data["provider"] == "anthropic"

def test_anthropic_adapter_api_missing_field():
    response = client.post(
        "/api/v1/models/anthropic",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_anthropic_adapter_api_error():
    response = client.post(
        "/api/v1/models/anthropic",
        json={"provider": "anthropic", "required_capabilities": ["unsupported"]},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "UNSUPPORTED"
    assert "Anthropic adapter conformance failed" in data["error"]["message"]
