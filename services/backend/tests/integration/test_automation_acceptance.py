from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_automation_acceptance_happy_path():
    payload = {
        "scenario": "morning-brief",
        "duplicate_trigger": True
    }
    response = client.post("/api/v1/quality/automation-acceptance", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["effective_runs"] == 1
    assert data["notification_count"] == 1

def test_integration_automation_acceptance_paused():
    payload = {
        "scenario": "paused",
        "duplicate_trigger": False
    }
    response = client.post("/api/v1/quality/automation-acceptance", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["effective_runs"] == 0
    assert data["notification_count"] == 0

def test_integration_automation_acceptance_missing_fields():
    response = client.post("/api/v1/quality/automation-acceptance", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
