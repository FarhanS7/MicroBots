from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_notification_inbox_happy_path():
    payload = {
        "event_id": "event-integration-1",
        "kind": "approval_required"
    }
    response = client.post("/api/v1/notifications/inbox", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["notification_id"] == "notification-1"
    assert data["unread"] is True

def test_integration_notification_inbox_duplicate():
    payload = {
        "event_id": "event-integration-1",
        "kind": "approval_required"
    }
    response = client.post("/api/v1/notifications/inbox", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["unread"] is False

def test_integration_notification_inbox_missing_fields():
    response = client.post("/api/v1/notifications/inbox", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
