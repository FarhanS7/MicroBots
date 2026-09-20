import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from oap.api.artifacts_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_artifact_revisions_api_happy_path():
    response = client.post(
        "/api/v1/artifacts/revisions",
        json={"artifact_id": "artifact-1", "restore_revision": 1, "expected_revision": 2},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["artifact_id"] == "artifact-1"
    assert data["revision"] == 3
    assert data["content_matches_revision"] == 1

def test_artifact_revisions_api_missing_field():
    response = client.post(
        "/api/v1/artifacts/revisions",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_artifact_revisions_api_conflict():
    response = client.post(
        "/api/v1/artifacts/revisions",
        json={"artifact_id": "artifact-1", "restore_revision": 1, "expected_revision": 1},
    )
    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "REVISION_CONFLICT"
    assert "Revision conflict detected" in data["error"]["message"]
