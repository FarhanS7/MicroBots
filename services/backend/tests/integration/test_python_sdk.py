from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_python_sdk_happy_path():
    payload = {
        "sdk_language": "python",
        "fixture": "read-record"
    }
    response = client.post("/api/v1/plugins/python-sdk", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["schema_valid"] is True
    assert data["contract_tests_passed"] is True

def test_integration_python_sdk_validation_error():
    payload = {
        "sdk_language": "python",
        "fixture": "incompatible-payload"
    }
    response = client.post("/api/v1/plugins/python-sdk", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_integration_python_sdk_missing_fields():
    response = client.post("/api/v1/plugins/python-sdk", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
