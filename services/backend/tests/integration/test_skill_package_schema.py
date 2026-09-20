import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

skills_router = pytest.importorskip("oap.api.skills_router", reason="Requires oap.api.skills_router owned by M04 (Skills Authoring)")
router = skills_router.router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_skill_package_schema_api_happy_path():
    response = client.post(
        "/api/v1/skills/schema",
        json={"name": "daily-brief", "version": "1.0.0", "required_tools": ["browser.read"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["skill_id"] == "skill-1"

def test_skill_package_schema_api_missing_field():
    response = client.post(
        "/api/v1/skills/schema",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_skill_package_schema_api_invalid():
    response = client.post(
        "/api/v1/skills/schema",
        json={"name": "daily-brief", "version": "1.0.0", "required_tools": ["unknown_tool"]},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "Invalid skill package manifest" in data["error"]["message"]
