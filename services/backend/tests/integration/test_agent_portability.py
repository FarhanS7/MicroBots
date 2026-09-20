import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_agent_portability_api_happy():
    payload = {
        "agent_id": "agent-1",
        "include_private_data": False
    }
    response = client.post("/api/v1/templates/portability", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["template_id"] == "template-1"
    assert data["secrets_included"] is False
    assert data["history_included"] is False

def test_agent_portability_api_missing():
    response = client.post("/api/v1/templates/portability", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
