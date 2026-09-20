from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_timezone_schedule_preview_happy_path():
    payload = {
        "schedule": "0 8 * * 1-5",
        "timezone": "Asia/Dhaka",
        "after": "2026-09-20T00:00:00Z"
    }
    response = client.post("/api/v1/automation/schedule-preview", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["next_run"] == "2026-09-21T02:00:00Z"

def test_integration_timezone_schedule_preview_validation_error():
    payload = {
        "schedule": "invalid",
        "timezone": "Asia/Dhaka",
        "after": "2026-09-20T00:00:00Z"
    }
    response = client.post("/api/v1/automation/schedule-preview", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_integration_timezone_schedule_preview_missing_fields():
    response = client.post("/api/v1/automation/schedule-preview", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
