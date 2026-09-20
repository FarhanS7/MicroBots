from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_oauth_lifecycle_happy_path():
    payload = {
        "connector_id": "connector-1",
        "callback_state": "fixture-state-integration",
        "code": "fixture-code"
    }
    response = client.post("/api/v1/connectors/oauth", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["connected"] is True
    assert data["secret_id"] == "oauth-secret-1"

def test_integration_oauth_lifecycle_validation_error():
    payload = {
        "connector_id": "connector-1",
        "callback_state": "wrong-state",
        "code": "fixture-code"
    }
    response = client.post("/api/v1/connectors/oauth", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_integration_oauth_lifecycle_missing_fields():
    response = client.post("/api/v1/connectors/oauth", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
