import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from oap.api.browser_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_browser_script_inspection_api_happy_path():
    response = client.post(
        "/api/v1/browser/inspect",
        json={"page_id": "page-1", "operation": "inspect-network"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["request_count"] == 2
    assert data["credentials_redacted"] is True

def test_browser_script_inspection_api_missing_field():
    response = client.post(
        "/api/v1/browser/inspect",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_browser_script_inspection_api_forbidden():
    response = client.post(
        "/api/v1/browser/inspect",
        json={"page_id": "page-1", "operation": "forbidden"},
    )
    assert response.status_code == 403
    data = response.json()
    assert data["error"]["code"] == "FORBIDDEN"
    assert "Script or network inspection capability forbidden" in data["error"]["message"]
