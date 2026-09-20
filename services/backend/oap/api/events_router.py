from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.events.transactional_outbox import F09Input, F09Output, transactional_outbox
from oap.events.resumable_activity_stream import (
    F22Input,
    F22Output,
    ResyncRequiredError,
    resumable_activity_stream,
)
from oap.events.authenticated_event_triggers import (
    A10Input,
    A10Output,
    authenticated_event_triggers,
)
from oap.events.file_watch_trigger import (
    A15Input,
    A15Output,
    file_watch_trigger,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/events", tags=["events"])

@router.post("/outbox", response_model=F09Output)
async def publish_outbox(raw_body: Dict[str, Any]) -> F09Output | JSONResponse:
    if "aggregate_id" not in raw_body or "event_type" not in raw_body or "request_id" not in raw_body:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Required input fields are missing",
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

    if not raw_body["aggregate_id"] or not raw_body["event_type"] or not raw_body["request_id"]:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Required input fields are missing",
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

    input_data = F09Input(**raw_body)
    return transactional_outbox(input_data)

@router.post("/stream", response_model=None)
async def stream_activity_events(raw_body: Dict[str, Any]) -> F22Output | JSONResponse:
    required_keys = ["after", "workspace_id"]
    if not all(k in raw_body and raw_body[k] is not None for k in required_keys):
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Required input fields are missing",
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

    try:
        input_data = F22Input(**raw_body)
        return resumable_activity_stream(input_data)
    except ResyncRequiredError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="RESYNC_REQUIRED",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/triggers", response_model=None)
async def trigger_event(raw_body: Dict[str, Any]) -> A10Output | JSONResponse:
    required_keys = ["subscription_id", "delivery_id", "event_type"]
    if not all(k in raw_body and raw_body[k] for k in required_keys):
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Required input fields are missing",
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

    input_data = A10Input(**raw_body)
    return authenticated_event_triggers(input_data)

@router.post("/watch", response_model=None)
async def watch_file_event(raw_body: Dict[str, Any]) -> A15Output | JSONResponse:
    required_keys = ["file_id", "revision"]
    if not all(k in raw_body and raw_body[k] is not None for k in required_keys):
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Required input fields are missing",
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

    input_data = A15Input(**raw_body)
    return file_watch_trigger(input_data)
