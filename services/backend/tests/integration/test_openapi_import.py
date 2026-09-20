from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_openapi_import_happy_path():
    payload = {
        "spec_id": "spec-1",
        "operation_ids": ["listRecords"]
    }
    response = client.post("/api/v1/connectors/openapi", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["tool_names"] == ["crm.listRecords"]
    assert data["enabled"] is False

def test_integration_openapi_import_validation_error():
    payload = {
        "spec_id": "private_spec",
        "operation_ids": ["listRecords"]
    }
    response = client.post("/api/v1/connectors/openapi", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_integration_openapi_import_missing_fields():
    response = client.post("/api/v1/connectors/openapi", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
