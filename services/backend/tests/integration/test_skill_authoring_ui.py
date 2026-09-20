from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_skill_authoring_ui_happy_path():
    payload = {
        "draft_id": "draft-1",
        "action": "review"
    }
    response = client.post("/api/v1/web/skill-authoring", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["active"] is False
    assert data["required_tools_visible"] is True

def test_integration_skill_authoring_ui_validation_error():
    payload = {
        "draft_id": "draft-1",
        "action": "activate_invalid"
    }
    response = client.post("/api/v1/web/skill-authoring", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_integration_skill_authoring_ui_missing_fields():
    response = client.post("/api/v1/web/skill-authoring", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
