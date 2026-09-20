import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from oap.api.browser_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_browser_action_suite_api_happy_path():
    response = client.post(
        "/api/v1/browser/action",
        json={"page_id": "page-1", "action": "click", "target": "fixture-button"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["clicked"] is True
    assert data["page_revision"] == 2

def test_browser_action_suite_api_missing_field():
    response = client.post(
        "/api/v1/browser/action",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_browser_action_suite_api_user_challenge():
    response = client.post(
        "/api/v1/browser/action",
        json={"page_id": "page-1", "action": "click", "target": "captcha"},
    )
    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "WAITING_USER"
    assert "Login challenge requires user interaction" in data["error"]["message"]
