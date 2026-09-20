from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_routine_history_retry_happy_path():
    payload = {
        "execution_id": "execution-1",
        "failure_code": "PROVIDER_UNAVAILABLE",
        "attempt": 1
    }
    response = client.post("/api/v1/automation/retry", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["retry_scheduled"] is True
    assert data["next_attempt"] == 2

def test_integration_routine_history_retry_non_retryable():
    payload = {
        "execution_id": "execution-1",
        "failure_code": "UNKNOWN_EXTERNAL_RESULT",
        "attempt": 1
    }
    response = client.post("/api/v1/automation/retry", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["retry_scheduled"] is False
    assert data["next_attempt"] == 1

def test_integration_routine_history_retry_missing_fields():
    response = client.post("/api/v1/automation/retry", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
