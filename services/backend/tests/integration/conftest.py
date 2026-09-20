"""Integration test fixtures."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def integration_app() -> FastAPI:
    """Shared integration application fixture."""
    app = FastAPI(title="MicroBots Integration App", version="0.1.0")
    return app


@pytest.fixture
def integration_client(integration_app: FastAPI) -> TestClient:
    """Shared integration TestClient fixture."""
    return TestClient(integration_app)
