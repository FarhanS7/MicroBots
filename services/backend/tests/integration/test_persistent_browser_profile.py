import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

browser_router = pytest.importorskip("oap.api.browser_router", reason="Requires oap.api.browser_router owned by M03 (Browser Automation)")
router = browser_router.router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_persistent_browser_profile_api_happy_path():
    response = client.post(
        "/api/v1/browser/profile",
        json={"profile_id": "profile-1", "persist": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["reusable"] is True
    assert data["workspace_id"] == "ws-1"

def test_persistent_browser_profile_api_missing_field():
    response = client.post(
        "/api/v1/browser/profile",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_persistent_browser_profile_api_lease_conflict():
    response = client.post(
        "/api/v1/browser/profile",
        json={"profile_id": "locked", "persist": True},
    )
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "CONFLICT"
    assert "Active browser profile lease already exists" in data["error"]["message"]
