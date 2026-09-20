from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_automation_ui_happy_path():
    payload = {
        "routine_id": "routine-1",
        "action": "pause"
    }
    response = client.post("/api/v1/web/automation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["visible_state"] == "paused"
    assert data["next_run"] is None

def test_integration_automation_ui_draft():
    payload = {
        "routine_id": "routine-1",
        "action": "unconfirmed_schedule"
    }
    response = client.post("/api/v1/web/automation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["visible_state"] == "draft"

def test_integration_automation_ui_missing_fields():
    response = client.post("/api/v1/web/automation", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
