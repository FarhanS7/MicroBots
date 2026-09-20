import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main import app
from oap.identity.local_owner_session import reset_owner_store

client = TestClient(app)

def setup_function() -> None:
    reset_owner_store()

def test_session_happy_path() -> None:
    response = client.post(
        "/api/v1/identity/session",
        json={"email": "owner@example.test", "password": "fixture-only-password"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "user_id": "user-1",
        "workspace_id": "ws-1",
        "authenticated": True,
    }

def test_session_missing_field() -> None:
    response = client.post("/api/v1/identity/session", json={})
    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Required input fields are missing",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }

def test_session_revision_conflict() -> None:
    client.post(
        "/api/v1/identity/setup",
        json={"email": "owner@example.test", "password": "fixture-only-password"},
    )
    response = client.post(
        "/api/v1/identity/setup",
        json={"email": "owner2@example.test", "password": "another-password"},
    )
    assert response.status_code == 409
    assert response.json() == {
        "error": {
            "code": "REVISION_CONFLICT",
            "message": "Owner account already configured",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }
