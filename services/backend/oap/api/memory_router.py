from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.memory.memory_governance import (
    P09Input,
    P09Output,
    MemoryDisabledError,
    memory_governance,
)
from oap.memory.scoped_memory_retrieval import (
    P10Input,
    P10Output,
    MemoryRetrievalError,
    scoped_memory_retrieval,
)
from oap.memory.retention_deletion_worker import (
    P27Input,
    P27Output,
    retention_deletion_worker,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/memory", tags=["memory"])

@router.post("/govern", response_model=None)
async def handle_memory_governance(raw_body: Dict[str, Any]) -> P09Output | JSONResponse:
    required_keys = ["category", "text", "source_message_id"]
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
        input_data = P09Input(**raw_body)
        return memory_governance(input_data)
    except MemoryDisabledError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="MEMORY_DISABLED",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/retrieve", response_model=None)
async def handle_scoped_memory_retrieval(raw_body: Dict[str, Any]) -> P10Output | JSONResponse:
    required_keys = ["query", "limit"]
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
        input_data = P10Input(**raw_body)
        return scoped_memory_retrieval(input_data)
    except MemoryRetrievalError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/purge", response_model=None)
async def handle_retention_deletion_worker(raw_body: Dict[str, Any]) -> P27Output | JSONResponse:
    required_keys = ["memory_id", "action"]
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

    input_data = P27Input(**raw_body)
    return retention_deletion_worker(input_data)
