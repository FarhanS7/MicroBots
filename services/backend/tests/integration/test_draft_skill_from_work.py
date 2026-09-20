import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

skills_router = pytest.importorskip("oap.api.skills_router", reason="Requires oap.api.skills_router owned by M04 (Skills Authoring)")
router = skills_router.router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_draft_skill_from_work_api_happy_path():
    response = client.post(
        "/api/v1/skills/draft",
        json={"source_task_id": "task-1", "name": "research-report"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["draft_id"] == "draft-1"
    assert data["active"] is False

def test_draft_skill_from_work_api_missing_field():
    response = client.post(
        "/api/v1/skills/draft",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
