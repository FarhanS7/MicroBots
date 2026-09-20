import pytest
from fastapi.testclient import TestClient
from main import app
from oap.artifacts.artifact_registration import reset_artifact_store

client = TestClient(app)

def setup_function():
    reset_artifact_store()

def test_artifacts_happy_path():
    payload = {
        "task_id": "task-1",
        "path": "report.md",
        "media_type": "text/markdown",
    }
    response = client.post("/api/v1/artifacts/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["artifact_id"] == "artifact-1"
    assert data["revision"] == 1
    assert data["downloadable"] is True

def test_artifacts_missing_file():
    payload = {
        "task_id": "task-1",
        "path": "nonexistent_file.png",
        "media_type": "image/png",
    }
    response = client.post("/api/v1/artifacts/register", json=payload)
    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "NOT_FOUND"

def test_artifacts_missing_field():
    response = client.post("/api/v1/artifacts/register", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
