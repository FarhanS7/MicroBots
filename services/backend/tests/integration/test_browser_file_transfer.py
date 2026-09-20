import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from oap.api.browser_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_browser_file_transfer_api_happy_path():
    response = client.post(
        "/api/v1/browser/transfer",
        json={"page_id": "page-1", "action": "download", "target": "fixture-report"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["file_id"] == "file-1"
    assert data["quarantined"] is True

def test_browser_file_transfer_api_missing_field():
    response = client.post(
        "/api/v1/browser/transfer",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_browser_file_transfer_api_unapproved():
    response = client.post(
        "/api/v1/browser/transfer",
        json={"page_id": "page-1", "action": "download", "target": "unapproved"},
    )
    assert response.status_code == 403
    data = response.json()
    assert data["error"]["code"] == "FORBIDDEN"
    assert "Destination not approved by policy" in data["error"]["message"]
