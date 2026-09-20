import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from oap.api.workflows_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_hybrid_workflow_runner_api_happy_path():
    response = client.post(
        "/api/v1/workflows/run",
        json={"workflow_id": "workflow-1", "version": 1, "input": {"topic": "databases"}},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["run_id"] == "workflow-run-1"
    assert data["state"] == "waiting_approval"

def test_hybrid_workflow_runner_api_missing_field():
    response = client.post(
        "/api/v1/workflows/run",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
