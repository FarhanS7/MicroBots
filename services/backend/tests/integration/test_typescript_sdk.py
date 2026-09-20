from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_typescript_sdk_happy_path():
    payload = {
        "sdk_language": "typescript",
        "fixture": "read-record"
    }
    response = client.post("/api/v1/plugins/ts-sdk", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["schema_valid"] is True
    assert data["contract_tests_passed"] is True

def test_integration_typescript_sdk_validation_error():
    payload = {
        "sdk_language": "typescript",
        "fixture": "incompatible-version"
    }
    response = client.post("/api/v1/plugins/ts-sdk", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_integration_typescript_sdk_missing_fields():
    response = client.post("/api/v1/plugins/ts-sdk", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
