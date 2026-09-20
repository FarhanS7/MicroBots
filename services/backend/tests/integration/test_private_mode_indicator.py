import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from oap.api.web_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_private_mode_indicator_api_happy_path():
    response = client.post(
        "/api/v1/web/private-mode",
        json={"privacy_mode": "local_only", "provider_id": "local-1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["external_model_contact"] is False
    assert data["indicator"] == "local-only"

def test_private_mode_indicator_api_missing_field():
    response = client.post(
        "/api/v1/web/private-mode",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_private_mode_indicator_api_incompatible():
    response = client.post(
        "/api/v1/web/private-mode",
        json={"privacy_mode": "local_only", "provider_id": "openai-cloud"},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "Incompatible remote provider under local-only mode" in data["error"]["message"]
