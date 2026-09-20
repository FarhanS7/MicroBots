from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.files.workspace_file_operations import (
    F17Input,
    F17Output,
    TraversalError,
    workspace_file_operations,
)
from oap.files.workspace_move_directories import (
    P28Input,
    P28Output,
    DestinationExistsConflictError,
    workspace_move_directories,
)
from oap.files.shared_file_conflicts import (
    C07Input,
    C07Output,
    RevisionConflictError,
    shared_file_conflicts,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/files", tags=["files"])

@router.post("/workspace", response_model=None)
async def perform_workspace_file_operation(raw_body: Dict[str, Any]) -> F17Output | JSONResponse:
    required_keys = ["path", "content", "expected_revision"]
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
        input_data = F17Input(**raw_body)
        return workspace_file_operations(input_data)
    except TraversalError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="FORBIDDEN",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=envelope.model_dump())

@router.post("/move", response_model=None)
async def move_workspace_entry(raw_body: Dict[str, Any]) -> P28Output | JSONResponse:
    required_keys = ["source", "destination", "expected_revision"]
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
        input_data = P28Input(**raw_body)
        return workspace_move_directories(input_data)
    except DestinationExistsConflictError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="REVISION_CONFLICT",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=envelope.model_dump())

@router.post("/shared/write", response_model=None)
async def handle_shared_file_conflicts(raw_body: Dict[str, Any]) -> C07Output | JSONResponse:
    required_keys = ["path", "expected_revision", "content"]
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
        input_data = C07Input(**raw_body)
        return shared_file_conflicts(input_data)
    except RevisionConflictError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="REVISION_CONFLICT",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=envelope.model_dump())

