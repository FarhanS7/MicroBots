import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from oap.api.web_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_usage_budget_ui_api_happy_path():
    response = client.post(
        "/api/v1/web/usage-budget",
        json={"task_id": "task-1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["spent_micro_usd"] == 100
    assert data["reserved_micro_usd"] == 200
    assert data["cost_known"] is True

def test_usage_budget_ui_api_missing_field():
    response = client.post(
        "/api/v1/web/usage-budget",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_usage_budget_ui_api_unknown_cost():
    response = client.post(
        "/api/v1/web/usage-budget",
        json={"task_id": "unknown_cost"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["cost_known"] is False
