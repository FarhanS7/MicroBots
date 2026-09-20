from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_integration_catalog_provenance_happy_path():
    payload = {
        "query": "research",
        "package_type": "skill"
    }
    response = client.post("/api/v1/marketplace/catalog", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["package_ids"] == ["package-1"]
    assert data["next_cursor"] is None

def test_integration_catalog_provenance_validation_error():
    payload = {
        "query": "withdrawn_malicious",
        "package_type": "skill"
    }
    response = client.post("/api/v1/marketplace/catalog", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"

def test_integration_catalog_provenance_missing_fields():
    response = client.post("/api/v1/marketplace/catalog", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
