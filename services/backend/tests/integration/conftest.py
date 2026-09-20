"""Integration test fixtures providing production app setup for integration suites."""

import importlib
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def integration_app() -> FastAPI:
    """
    Shared integration application fixture.
    Attempts to import the central application factory (oap.app) once R05 completes,
    falling back to a baseline FastAPI application container.
    """
    try:
        app_module = importlib.import_module("oap.app")
        create_app = getattr(app_module, "create_app", None)
        if callable(create_app):
            return create_app()
    except ImportError:
        pass

    app = FastAPI(title="MicroBots Integration App", version="0.1.0")
    return app


@pytest.fixture
def integration_client(integration_app: FastAPI) -> TestClient:
    """Shared integration TestClient fixture."""
    return TestClient(integration_app)
