from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.tasks.durable_task_submission import (
    F14Input,
    F14Output,
    TaskIdempotencyConflictError,
    durable_task_submission,
)
from oap.tasks.task_control import (
    P06Input,
    P06Output,
    TaskControlError,
    task_control,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

@router.post("", response_model=F14Output)
async def submit_task(raw_body: Dict[str, Any]) -> F14Output | JSONResponse:
    required_keys = ["agent_id", "instruction", "idempotency_key"]
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
        input_data = F14Input(**raw_body)
        return durable_task_submission(input_data)
    except TaskIdempotencyConflictError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="IDEMPOTENCY_CONFLICT",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=envelope.model_dump())

@router.post("/control", response_model=None)
async def control_task(raw_body: Dict[str, Any]) -> P06Output | JSONResponse:
    required_keys = ["task_id", "action", "expected_revision"]
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
        input_data = P06Input(**raw_body)
        return task_control(input_data)
    except TaskControlError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

