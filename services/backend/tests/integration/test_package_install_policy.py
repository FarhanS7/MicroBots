import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

execution_router = pytest.importorskip("oap.api.execution_router", reason="Requires oap.api.execution_router owned by M03 (Execution Router)")
router = execution_router.router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_package_install_policy_api_happy_path():
    response = client.post(
        "/api/v1/execution/packages",
        json={"manager": "pip", "package": "fixture-package", "environment": "sandbox-1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["installed"] is True
    assert data["host_modified"] is False

def test_package_install_policy_api_missing_field():
    response = client.post(
        "/api/v1/execution/packages",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"

def test_package_install_policy_api_forbidden():
    response = client.post(
        "/api/v1/execution/packages",
        json={"manager": "pip", "package": "forbidden", "environment": "sandbox-1"},
    )
    assert response.status_code == 403
    data = response.json()
    assert data["error"]["code"] == "FORBIDDEN"
    assert "Package installation forbidden" in data["error"]["message"]
