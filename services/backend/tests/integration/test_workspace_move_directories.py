import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

files_router = pytest.importorskip("oap.api.files_router", reason="Requires oap.api.files_router owned by M02 (File Operations)")
router = files_router.router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_workspace_move_directories_api_happy_path():
    response = client.post(
        "/api/v1/files/move",
        json={"source": "notes.md", "destination": "research/notes.md", "expected_revision": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["path"] == "research/notes.md"
    assert data["revision"] == 2

def test_workspace_move_directories_api_missing_field():
    response = client.post(
        "/api/v1/files/move",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_workspace_move_directories_api_conflict():
    response = client.post(
        "/api/v1/files/move",
        json={"source": "notes.md", "destination": "existing/notes.md", "expected_revision": 1},
    )
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "REVISION_CONFLICT"
    assert "Destination collision or revision conflict" in data["error"]["message"]
