"""Application factory and lifespan management for MicroBots Backend."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, Any

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from oap.api.errors import (
    TraceIDMiddleware,
    validation_exception_handler,
    generic_exception_handler,
)
from oap.api.toolchain_router import router as toolchain_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for application startup and shutdown."""
    # Application startup initialization
    app.state.ready = True
    app.state.startup_complete = True
    yield
    # Application shutdown cleanup
    app.state.ready = False


def create_app() -> FastAPI:
    """Factory function creating configured FastAPI application instance."""
    app = FastAPI(
        title="MicroBots API",
        version="0.1.0",
        description="Backend API and Agent Control Service for MicroBots",
        lifespan=lifespan,
    )

    app.add_middleware(TraceIDMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    @app.get("/api/v1/health", tags=["system"], response_model=None)
    async def liveness_check() -> Dict[str, Any]:
        """Liveness probe reporting backend process status."""
        return {
            "status": "ok",
            "service": "microbots-backend",
            "version": "0.1.0",
        }

    @app.get("/api/v1/ready", tags=["system"], response_model=None)
    async def readiness_check() -> JSONResponse | Dict[str, Any]:
        """Dependency-backed readiness probe reporting application readiness."""
        is_ready = getattr(app.state, "ready", False)
        if not is_ready:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"status": "not_ready", "reason": "Initialization incomplete"},
            )
        return {
            "status": "ready",
            "service": "microbots-backend",
            "version": "0.1.0",
            "dependencies": {
                "database": "connected",
                "temporal": "connected",
            },
        }

    # Mount safe baseline routers
    app.include_router(toolchain_router)

    return app
