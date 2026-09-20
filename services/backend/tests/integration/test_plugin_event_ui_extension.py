from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_plugin_event_ui_extension_happy_path():
    payload = {
        "plugin_id": "plugin-1",
        "event_type": "task.completed"
    }
    response = client.post("/api/v1/plugins/events", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["subscription_id"] == "plugin-subscription-1"
    assert data["scope"] == "ws-1"

def test_integration_plugin_event_ui_extension_validation_error():
    payload = {
        "plugin_id": "plugin-1",
        "event_type": "unauthorized_cross_workspace"
    }
    response = client.post("/api/v1/plugins/events", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_integration_plugin_event_ui_extension_missing_fields():
    response = client.post("/api/v1/plugins/events", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
