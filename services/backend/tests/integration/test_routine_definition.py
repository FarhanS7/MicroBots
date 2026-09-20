from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_routine_definition_happy_path():
    payload = {
        "name": "Morning brief",
        "timezone": "Asia/Dhaka",
        "trigger": "scheduled",
        "cron": "0 8 * * 1-5"
    }
    response = client.post("/api/v1/automation/routines", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["routine_id"] == "routine-1"
    assert data["enabled"] is False

def test_integration_routine_definition_validation_error():
    payload = {
        "name": "Morning brief",
        "timezone": "invalid/timezone",
        "trigger": "scheduled",
        "cron": "0 8 * * 1-5"
    }
    response = client.post("/api/v1/automation/routines", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_integration_routine_definition_missing_fields():
    response = client.post("/api/v1/automation/routines", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
