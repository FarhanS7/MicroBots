from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_connector_registry_happy_path():
    payload = {
        "name": "fixture-crm",
        "auth_type": "api_key",
        "secret_id": "secret-1"
    }
    response = client.post("/api/v1/connectors/registry", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["connector_id"] == "connector-1"
    assert data["enabled"] is False

def test_integration_connector_registry_validation_error():
    payload = {
        "name": "fixture-crm",
        "auth_type": "unknown",
        "secret_id": "secret-1"
    }
    response = client.post("/api/v1/connectors/registry", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_integration_connector_registry_missing_fields():
    response = client.post("/api/v1/connectors/registry", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
