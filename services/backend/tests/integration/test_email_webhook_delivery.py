from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_email_webhook_delivery_happy_path():
    payload = {
        "notification_id": "notification-1",
        "channel": "webhook",
        "destination_id": "destination-1"
    }
    response = client.post("/api/v1/notifications/delivery", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["delivery_id"] == "delivery-1"
    assert data["state"] == "queued"

def test_integration_email_webhook_delivery_validation_error():
    payload = {
        "notification_id": "notification-1",
        "channel": "webhook",
        "destination_id": "unauthorized-destination"
    }
    response = client.post("/api/v1/notifications/delivery", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_integration_email_webhook_delivery_missing_fields():
    response = client.post("/api/v1/notifications/delivery", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
