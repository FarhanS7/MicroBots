from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.automation.routine_definition import (
    A06Input,
    A06Output,
    InvalidRoutineDefinitionError,
    routine_definition,
)
from oap.automation.timezone_schedule_preview import (
    A07Input,
    A07Output,
    InvalidTimezoneScheduleError,
    timezone_schedule_preview,
)
from oap.automation.routine_dispatch_control import (
    A08Input,
    A08Output,
    routine_dispatch_control,
)
from oap.automation.routine_history_retry import (
    A09Input,
    A09Output,
    routine_history_retry,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/automation", tags=["automation"])

@router.post("/routines", response_model=None)
async def create_routine_definition(raw_body: Dict[str, Any]) -> A06Output | JSONResponse:
    required_keys = ["name", "timezone", "trigger", "cron"]
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

    try:
        input_data = A06Input(**raw_body)
        return routine_definition(input_data)
    except InvalidRoutineDefinitionError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/schedule-preview", response_model=None)
async def preview_schedule(raw_body: Dict[str, Any]) -> A07Output | JSONResponse:
    required_keys = ["schedule", "timezone", "after"]
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

    try:
        input_data = A07Input(**raw_body)
        return timezone_schedule_preview(input_data)
    except InvalidTimezoneScheduleError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/dispatch", response_model=None)
async def dispatch_routine(raw_body: Dict[str, Any]) -> A08Output | JSONResponse:
    required_keys = ["routine_id", "scheduled_for"]
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

    input_data = A08Input(**raw_body)
    return routine_dispatch_control(input_data)

@router.post("/retry", response_model=None)
async def retry_routine(raw_body: Dict[str, Any]) -> A09Output | JSONResponse:
    required_keys = ["execution_id", "failure_code", "attempt"]
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

    input_data = A09Input(**raw_body)
    return routine_history_retry(input_data)
