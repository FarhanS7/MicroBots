import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

web_router = pytest.importorskip("oap.api.web_router", reason="Requires oap.api.web_router owned by M01 (Web UI)")
router = web_router.router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_model_settings_ui_api_happy_path():
    response = client.post(
        "/api/v1/web/model-settings",
        json={"provider_id": "local-1", "privacy_mode": "local_only"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["saved"] is True
    assert data["locality_indicator"] == "local"

def test_model_settings_ui_api_missing_field():
    response = client.post(
        "/api/v1/web/model-settings",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_model_settings_ui_api_connection_error():
    response = client.post(
        "/api/v1/web/model-settings",
        json={"provider_id": "unreachable", "privacy_mode": "cloud_allowed"},
    )
    assert response.status_code == 503
    data = response.json()
    assert data["error"]["code"] == "SERVICE_UNAVAILABLE"
    assert "Provider endpoint connectivity failed" in data["error"]["message"]
