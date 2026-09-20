import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main import app

client = TestClient(app)

def test_models_happy_path() -> None:
    response = client.post(
        "/api/v1/models/capability",
        json={"provider_id": "provider-1", "required_capabilities": ["tools"]},
    )
    assert response.status_code == 200
    assert response.json() == {
        "compatible": True,
        "provider_id": "provider-1",
    }

def test_models_capability_unsupported() -> None:
    response = client.post(
        "/api/v1/models/capability",
        json={"provider_id": "text-only-provider", "required_capabilities": ["tools"]},
    )
    assert response.status_code == 422
    assert response.json() == {
        "error": {
            "code": "CAPABILITY_UNSUPPORTED",
            "message": "Capabilities unsupported by provider: ['tools']",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }

def test_models_missing_field() -> None:
    response = client.post("/api/v1/models/capability", json={})
    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Required input fields are missing",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }
