from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_plugin_manifest_runtime_happy_path():
    payload = {
        "name": "fixture-plugin",
        "version": "1.0.0",
        "permissions": ["network:fixture.example.test"]
    }
    response = client.post("/api/v1/plugins/manifest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["installed"] is False

def test_integration_plugin_manifest_runtime_validation_error():
    payload = {
        "name": "fixture-plugin",
        "version": "1.0.0",
        "permissions": ["undeclared_network"]
    }
    response = client.post("/api/v1/plugins/manifest", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_integration_plugin_manifest_runtime_missing_fields():
    response = client.post("/api/v1/plugins/manifest", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
