import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_file_global_search_api_happy():
    payload = {
        "query": "research",
        "types": ["file", "agent"],
        "limit": 10
    }
    response = client.post("/api/v1/search/global", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["result_ids"] == ["file-1", "agent-1"]
    assert data["next_cursor"] is None

def test_file_global_search_api_missing():
    response = client.post("/api/v1/search/global", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
