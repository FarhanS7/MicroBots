import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from oap.api.quality_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_mvp_recovery_acceptance_api_happy_path():
    response = client.post(
        "/api/v1/quality/mvp-recovery",
        json={"scenario": "five-database-projects", "disconnect_client": True, "restart_worker": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["artifact_valid"] is True
    assert data["conversation_persisted"] is True
    assert data["duplicate_effects"] == 0

def test_mvp_recovery_acceptance_api_missing_field():
    response = client.post(
        "/api/v1/quality/mvp-recovery",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_mvp_recovery_acceptance_api_denied():
    response = client.post(
        "/api/v1/quality/mvp-recovery",
        json={"scenario": "denied", "disconnect_client": True, "restart_worker": True},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "DENIED"
    assert "External login request was denied" in data["error"]["message"]
