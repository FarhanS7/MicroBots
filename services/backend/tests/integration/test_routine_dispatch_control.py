from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_routine_dispatch_control_happy_path():
    payload = {
        "routine_id": "routine-integration-1",
        "scheduled_for": "2026-09-21T02:00:00Z"
    }
    response = client.post("/api/v1/automation/dispatch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["execution_id"] == "execution-1"
    assert data["duplicate"] is False

def test_integration_routine_dispatch_control_duplicate():
    payload = {
        "routine_id": "routine-integration-1",
        "scheduled_for": "2026-09-21T02:00:00Z"
    }
    response = client.post("/api/v1/automation/dispatch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["duplicate"] is True

def test_integration_routine_dispatch_control_missing_fields():
    response = client.post("/api/v1/automation/dispatch", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
