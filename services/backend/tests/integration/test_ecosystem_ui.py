import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ecosystem_ui_api_happy():
    payload = {
        "package_id": "package-1",
        "action": "inspect-permissions"
    }
    response = client.post("/api/v1/web/ecosystem", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["permissions_visible"] is True
    assert data["activation_requires_confirmation"] is True

def test_ecosystem_ui_api_missing():
    response = client.post("/api/v1/web/ecosystem", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
