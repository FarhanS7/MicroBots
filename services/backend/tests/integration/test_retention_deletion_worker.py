import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from oap.api.memory_router import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_retention_deletion_worker_api_happy_path():
    response = client.post(
        "/api/v1/memory/purge",
        json={"memory_id": "memory-1", "action": "delete"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["memory_deleted"] is True
    assert data["derived_entries_deleted"] is True

def test_retention_deletion_worker_api_missing_field():
    response = client.post(
        "/api/v1/memory/purge",
        json={},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
