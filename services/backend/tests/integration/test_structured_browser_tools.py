import pytest
from fastapi.testclient import TestClient
from main import app
from oap.browser.structured_browser_tools import reset_browser_store

client = TestClient(app)

def setup_function():
    reset_browser_store()

def test_browser_happy_path():
    payload = {"url": "https://fixture.example.test/report"}
    response = client.post("/api/v1/browser/navigate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["page_id"] == "page-1"
    assert data["title"] == "Fixture report"
    assert data["text"] == "Revenue increased."

def test_browser_ssrf_blocked():
    payload = {"url": "http://169.254.169.254/latest/meta-data/"}
    response = client.post("/api/v1/browser/navigate", json=payload)
    assert response.status_code == 403
    data = response.json()
    assert data["error"]["code"] == "FORBIDDEN"
    assert "Private or metadata IP address blocked" in data["error"]["message"]

def test_browser_missing_field():
    response = client.post("/api/v1/browser/navigate", json={})
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Required input fields are missing"
    assert data["trace_id"] == "trace-test"
