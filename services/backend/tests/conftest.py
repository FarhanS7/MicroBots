"""Global pytest fixtures and layout configuration."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def base_app() -> FastAPI:
    """Baseline FastAPI application instance for integration fixtures."""
    app = FastAPI(title="MicroBots Backend Test App", version="0.1.0")
    return app


@pytest.fixture
def base_client(base_app: FastAPI) -> TestClient:
    """Baseline HTTP client fixture."""
    return TestClient(base_app)
