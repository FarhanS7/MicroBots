from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_authenticated_event_triggers_happy_path():
    payload = {
        "subscription_id": "subscription-1",
        "delivery_id": "delivery-integration-1",
        "event_type": "file.created"
    }
    response = client.post("/api/v1/events/triggers", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["accepted"] is True
    assert data["execution_id"] == "execution-1"

def test_integration_authenticated_event_triggers_duplicate():
    payload = {
        "subscription_id": "subscription-1",
        "delivery_id": "delivery-integration-1",
        "event_type": "file.created"
    }
    response = client.post("/api/v1/events/triggers", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["accepted"] is False

def test_integration_authenticated_event_triggers_missing_fields():
    response = client.post("/api/v1/events/triggers", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
