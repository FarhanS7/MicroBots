import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

web_router = pytest.importorskip("oap.api.web_router", reason="Requires oap.api.web_router owned by M01 (Task P26)")
router = web_router.router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_agent_configuration_ui_api_happy_path():
    response = client.post(
        "/api/v1/web/agent-config",
        json={"agent_id": "agent-1", "name": "Scout", "expected_revision": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["agent_id"] == "agent-1"
    assert data["name"] == "Scout"
    assert data["revision"] == 2

def test_agent_configuration_ui_api_missing_field():
    response = client.post(
        "/api/v1/web/agent-config",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_agent_configuration_ui_api_conflict():
    response = client.post(
        "/api/v1/web/agent-config",
        json={"agent_id": "agent-1", "name": "Scout", "expected_revision": 2},
    )
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "REVISION_CONFLICT"
    assert "Revision conflict on agent configuration" in data["error"]["message"]
