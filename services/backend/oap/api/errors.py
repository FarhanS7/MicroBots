"""Standardized error handlers and trace ID tracking for FastAPI."""

import uuid
from typing import Callable, Awaitable
from fastapi import Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail


class TraceIDMiddleware(BaseHTTPMiddleware):
    """Middleware attaching X-Trace-ID header to every request and response."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        trace_id = request.headers.get("X-Trace-ID") or f"trace-{uuid.uuid4().hex[:12]}"
        request.state.trace_id = trace_id
        response = await call_next(request)
        response.headers["X-Trace-ID"] = trace_id
        return response


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Exception handler converting Pydantic RequestValidationError into PublicErrorEnvelope."""
    trace_id = getattr(request.state, "trace_id", "trace-default")
    envelope = PublicErrorEnvelope(
        error=ErrorDetail(
            code="VALIDATION_ERROR",
            message="Invalid or malformed request payload",
            retryable=False,
        ),
        trace_id=trace_id,
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=envelope.model_dump(),
        headers={"X-Trace-ID": trace_id},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all exception handler converting unhandled errors into PublicErrorEnvelope."""
    trace_id = getattr(request.state, "trace_id", "trace-default")
    envelope = PublicErrorEnvelope(
        error=ErrorDetail(
            code="INTERNAL_ERROR",
            message="An internal server error occurred",
            retryable=True,
        ),
        trace_id=trace_id,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=envelope.model_dump(),
        headers={"X-Trace-ID": trace_id},
    )
