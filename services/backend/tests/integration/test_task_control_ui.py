import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

web_router = pytest.importorskip("oap.api.web_router", reason="Requires oap.api.web_router owned by M01 (Web UI)")
router = web_router.router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_task_control_ui_api_happy_path():
    response = client.post(
        "/api/v1/web/task-control",
        json={"task_id": "task-1", "action": "cancel"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["visible_state"] == "cancellation-requested"

def test_task_control_ui_api_missing_field():
    response = client.post(
        "/api/v1/web/task-control",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
