import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

web_router = pytest.importorskip("oap.api.web_router", reason="Requires oap.api.web_router owned by M01 (Web UI)")
router = web_router.router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_memory_governance_ui_api_happy_path():
    response = client.post(
        "/api/v1/web/memory",
        json={"panel": "memory", "delete_memory_id": "memory-1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["visible_memory_ids"] == []
    assert data["deletion_confirmed"] is True

def test_memory_governance_ui_api_missing_field():
    response = client.post(
        "/api/v1/web/memory",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_memory_governance_ui_api_stale_conflict():
    response = client.post(
        "/api/v1/web/memory",
        json={"panel": "memory", "delete_memory_id": "stale-1"},
    )
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "CONFLICT"
    assert "Stale memory edit conflict" in data["error"]["message"]
