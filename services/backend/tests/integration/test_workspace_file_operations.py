import pytest
from fastapi.testclient import TestClient
from main import app
from oap.files.workspace_file_operations import reset_file_store

client = TestClient(app)

def setup_function():
    reset_file_store()

def test_files_happy_path():
    payload = {
        "path": "report.md",
        "content": "# Research",
        "expected_revision": 0,
    }
    response = client.post("/api/v1/files/workspace", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["path"] == "report.md"
    assert data["revision"] == 1
    assert data["bytes"] == 10

def test_files_traversal_forbidden():
    payload = {
        "path": "../secret.txt",
        "content": "secret",
        "expected_revision": 0,
    }
    response = client.post("/api/v1/files/workspace", json=payload)
    assert response.status_code == 403
    data = response.json()
    assert data["error"]["code"] == "FORBIDDEN"
    assert "Path traversal or escaping symlink forbidden" in data["error"]["message"]

def test_files_missing_field():
    response = client.post("/api/v1/files/workspace", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
