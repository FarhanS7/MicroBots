import sys
import os
from unittest.mock import patch
from fastapi.testclient import TestClient

# Ensure services/backend is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main import app
from oap.domain.toolchain import PrerequisiteError

client = TestClient(app)

def test_toolchain_contract_happy_path() -> None:
    response = client.post("/api/v1/toolchain/verify", json={"environment": "local"})
    assert response.status_code == 200
    assert response.json() == {
        "python_locked": True,
        "javascript_locked": True,
        "docs_check_available": True,
    }

def test_toolchain_contract_missing_field() -> None:
    response = client.post("/api/v1/toolchain/verify", json={})
    assert response.status_code == 400
    assert response.json() == {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Required input fields are missing",
            "retryable": False,
        },
        "trace_id": "trace-test",
    }

def test_toolchain_contract_prerequisite_error() -> None:
    with patch("oap.api.toolchain_router.verify_toolchain_contract", side_effect=PrerequisiteError("Required toolchain runtime or lockfile is missing")):
        response = client.post("/api/v1/toolchain/verify", json={"environment": "local"})
        assert response.status_code == 412
        assert response.json() == {
            "error": {
                "code": "PREREQUISITE_ERROR",
                "message": "Required toolchain runtime or lockfile is missing",
                "retryable": False,
            },
            "trace_id": "trace-test",
        }
