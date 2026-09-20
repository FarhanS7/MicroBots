import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from oap.api.execution_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_background_process_control_api_happy_path():
    response = client.post(
        "/api/v1/execution/process",
        json={"command": "fixture-long-process", "background": True, "timeout_seconds": 30},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["process_id"] == "process-1"
    assert data["state"] == "running"

def test_background_process_control_api_missing_field():
    response = client.post(
        "/api/v1/execution/process",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_background_process_control_api_not_found():
    response = client.post(
        "/api/v1/execution/process",
        json={"command": "foreign-process", "background": True, "timeout_seconds": 30},
    )
    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "NOT_FOUND"
    assert "Background process not found" in data["error"]["message"]
