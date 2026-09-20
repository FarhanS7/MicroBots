from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_generic_http_auth_happy_path():
    payload = {
        "connector_id": "connector-1",
        "method": "GET",
        "path": "/records"
    }
    response = client.post("/api/v1/connectors/http", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["body"] == {"items": []}

def test_integration_generic_http_auth_validation_error():
    payload = {
        "connector_id": "connector-1",
        "method": "GET",
        "path": "/cross-origin-redirect"
    }
    response = client.post("/api/v1/connectors/http", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_integration_generic_http_auth_missing_fields():
    response = client.post("/api/v1/connectors/http", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
