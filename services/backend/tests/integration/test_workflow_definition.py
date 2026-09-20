import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

workflows_router = pytest.importorskip("oap.api.workflows_router", reason="Requires oap.api.workflows_router owned by M05 (Workflows)")
router = workflows_router.router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_workflow_definition_api_happy_path():
    response = client.post(
        "/api/v1/workflows/definition",
        json={"nodes": ["fetch", "summarize", "approve"], "edges": [["fetch", "summarize"], ["summarize", "approve"]]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["workflow_version"] == 1

def test_workflow_definition_api_missing_field():
    response = client.post(
        "/api/v1/workflows/definition",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_workflow_definition_api_unbounded_cycle():
    response = client.post(
        "/api/v1/workflows/definition",
        json={"nodes": ["fetch", "loop"], "edges": [["loop", "loop"]]},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "Unbounded cycle detected" in data["error"]["message"]
