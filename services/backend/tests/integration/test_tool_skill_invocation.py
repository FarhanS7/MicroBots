from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_tool_skill_invocation_happy_path():
    payload = {
        "message_id": "message-1",
        "skill_id": "skill-1",
        "version": "1.0.0"
    }
    response = client.post("/api/v1/conversation/tool-skill", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["invocation_id"] == "invocation-1"
    assert data["permission_widened"] is False

def test_integration_tool_skill_invocation_validation_error():
    payload = {
        "message_id": "message-1",
        "skill_id": "unauthorized-skill",
        "version": "1.0.0"
    }
    response = client.post("/api/v1/conversation/tool-skill", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_integration_tool_skill_invocation_missing_fields():
    response = client.post("/api/v1/conversation/tool-skill", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
