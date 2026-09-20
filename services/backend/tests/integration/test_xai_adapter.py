import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from oap.api.models_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_xai_adapter_api_happy_path():
    response = client.post(
        "/api/v1/models/xai",
        json={"provider": "xai", "required_capabilities": ["tools"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["conformance_passed"] is True
    assert data["provider"] == "xai"

def test_xai_adapter_api_missing_field():
    response = client.post(
        "/api/v1/models/xai",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_xai_adapter_api_error():
    response = client.post(
        "/api/v1/models/xai",
        json={"provider": "xai", "required_capabilities": ["rate_limit"]},
    )
    assert response.status_code == 429
    data = response.json()
    assert data["error"]["code"] == "RATE_LIMITED"
    assert "xAI rate limit exceeded" in data["error"]["message"]
