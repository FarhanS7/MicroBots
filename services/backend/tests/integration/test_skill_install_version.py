import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from oap.api.skills_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_skill_install_version_api_happy_path():
    response = client.post(
        "/api/v1/skills/install",
        json={"package": "fixture-daily-brief", "version": "1.0.0"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["installed_version"] == "1.0.0"
    assert data["enabled"] is False

def test_skill_install_version_api_missing_field():
    response = client.post(
        "/api/v1/skills/install",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_skill_install_version_api_unsafe():
    response = client.post(
        "/api/v1/skills/install",
        json={"package": "traversal-archive", "version": "1.0.0"},
    )
    assert response.status_code == 403
    data = response.json()
    assert data["error"]["code"] == "FORBIDDEN"
    assert "Unsafe archive or expanded permissions rejected" in data["error"]["message"]
