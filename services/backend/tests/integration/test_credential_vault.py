import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main import app
from oap.secrets.credential_vault import reset_vault, revoke_credential

client = TestClient(app)

def setup_function() -> None:
    reset_vault()

def test_secrets_happy_path() -> None:
    response = client.post(
        "/api/v1/secrets/vault",
        json={"provider": "compatible", "credential": "fake-test-key"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "secret_id": "secret-1",
        "configured": True,
    }

def test_secrets_revoked_forbidden() -> None:
    client.post(
        "/api/v1/secrets/vault",
        json={"provider": "compatible", "credential": "fake-test-key"},
    )
    revoke_credential("secret-1")
    response = client.post("/api/v1/secrets/resolve", json={"secret_id": "secret-1"})
    assert response.status_code == 403
    assert response.json() == {
        "error": {
            "code": "FORBIDDEN",
            "message": "Access to revoked credential handle is forbidden",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }

def test_secrets_missing_field() -> None:
    response = client.post("/api/v1/secrets/vault", json={})
    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Required input fields are missing",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }
