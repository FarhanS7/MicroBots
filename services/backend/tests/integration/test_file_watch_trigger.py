from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_file_watch_trigger_happy_path():
    payload = {
        "file_id": "file-integration-1",
        "revision": 2
    }
    response = client.post("/api/v1/events/watch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["event_type"] == "file.created"
    assert data["delivery_count"] == 1

def test_integration_file_watch_trigger_replay():
    payload = {
        "file_id": "file-integration-1",
        "revision": 2
    }
    response = client.post("/api/v1/events/watch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["delivery_count"] == 0

def test_integration_file_watch_trigger_missing_fields():
    response = client.post("/api/v1/events/watch", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
