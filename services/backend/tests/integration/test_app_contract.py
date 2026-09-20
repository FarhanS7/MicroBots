"""Integration contract tests for production application factory, health, readiness, and error handling."""

import pytest
from fastapi.testclient import TestClient

from oap.app import create_app


@pytest.fixture
def app_client() -> TestClient:
    app = create_app()
    with TestClient(app) as client:
        yield client


def test_liveness_probe_returns_200(app_client: TestClient) -> None:
    response = app_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "microbots-backend"
    assert data["version"] == "0.1.0"
    assert "X-Trace-ID" in response.headers


def test_readiness_probe_returns_200_when_booted(app_client: TestClient) -> None:
    response = app_client.get("/api/v1/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["dependencies"]["database"] == "connected"
    assert data["dependencies"]["temporal"] == "connected"


def test_custom_trace_id_header_preserved(app_client: TestClient) -> None:
    custom_trace = "trace-custom-123"
    response = app_client.get("/api/v1/health", headers={"X-Trace-ID": custom_trace})
    assert response.status_code == 200
    assert response.headers["X-Trace-ID"] == custom_trace


def test_cors_preflight_headers_present(app_client: TestClient) -> None:
    response = app_client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") in ["*", "http://localhost:3000"]
