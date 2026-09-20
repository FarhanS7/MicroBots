import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_web_artifact_happy_path():
    payload = {"artifact_id": "artifact-1", "media_type": "text/markdown"}
    response = client.post("/api/v1/web/artifact", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["preview_kind"] == "sanitized-markdown"
    assert data["download_enabled"] is True

def test_web_artifact_render_error():
    payload = {"artifact_id": "invalid", "media_type": "text/markdown"}
    response = client.post("/api/v1/web/artifact", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "PREVIEW_ERROR"

def test_web_artifact_missing_field():
    response = client.post("/api/v1/web/artifact", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
