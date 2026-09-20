import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_package_update_rollback_api_happy():
    payload = {
        "package_id": "package-1",
        "target_version": "1.1.0",
        "approved_permissions": ["browser.read"]
    }
    response = client.post("/api/v1/marketplace/update-rollback", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["installed_version"] == "1.1.0"
    assert data["rollback_version"] == "1.0.0"

def test_package_update_rollback_api_edge():
    payload = {
        "package_id": "unapproved_perm_package",
        "target_version": "1.1.0",
        "approved_permissions": ["browser.read"]
    }
    response = client.post("/api/v1/marketplace/update-rollback", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "unapproved permissions" in data["error"]["message"]

def test_package_update_rollback_api_missing():
    response = client.post("/api/v1/marketplace/update-rollback", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
