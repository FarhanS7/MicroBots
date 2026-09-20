from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_mcp_client_happy_path():
    payload = {
        "server_id": "mcp-1",
        "tool": "fixture.read",
        "arguments": {
            "id": "record-1"
        }
    }
    response = client.post("/api/v1/connectors/mcp", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == {"name": "Fixture"}
    assert data["validated"] is True

def test_integration_mcp_client_validation_error():
    payload = {
        "server_id": "mcp-1",
        "tool": "invalid_schema_tool",
        "arguments": {
            "id": "record-1"
        }
    }
    response = client.post("/api/v1/connectors/mcp", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_integration_mcp_client_missing_fields():
    response = client.post("/api/v1/connectors/mcp", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
