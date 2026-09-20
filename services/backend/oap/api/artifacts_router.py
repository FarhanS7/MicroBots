from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.artifacts.artifact_registration import (
    F21Input,
    F21Output,
    ArtifactNotFoundError,
    artifact_registration,
)
from oap.artifacts.artifact_revisions import (
    P14Input,
    P14Output,
    RevisionConflictError,
    artifact_revisions,
)
from oap.artifacts.rich_artifact_handlers import (
    I18Input,
    I18Output,
    QuarantinedArtifactError,
    rich_artifact_handlers,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/artifacts", tags=["artifacts"])

@router.post("/register", response_model=None)
async def register_artifact(raw_body: Dict[str, Any]) -> F21Output | JSONResponse:
    required_keys = ["task_id", "path", "media_type"]
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
        input_data = F21Input(**raw_body)
        return artifact_registration(input_data)
    except ArtifactNotFoundError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="NOT_FOUND",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=envelope.model_dump())

@router.post("/revisions", response_model=None)
async def restore_artifact_revision(raw_body: Dict[str, Any]) -> P14Output | JSONResponse:
    required_keys = ["artifact_id", "restore_revision", "expected_revision"]
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
        input_data = P14Input(**raw_body)
        return artifact_revisions(input_data)
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

@router.post("/handlers", response_model=None)
async def handle_rich_artifact_handlers(raw_body: Dict[str, Any]) -> I18Output | JSONResponse:
    required_keys = ["artifact_id", "media_type"]
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
        input_data = I18Input(**raw_body)
        return rich_artifact_handlers(input_data)
    except QuarantinedArtifactError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="QUARANTINED",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

from oap.storage.s3_storage_adapter import (
    O02Input,
    O02Output,
    StorageError,
    s3_storage_adapter,
)

@router.post("/s3-storage", response_model=None)
async def store_s3_artifact(raw_body: Dict[str, Any]) -> O02Output | JSONResponse:
    required_keys = ["artifact_id", "backend"]
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
        input_data = O02Input(**raw_body)
        return s3_storage_adapter(input_data)
    except StorageError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="STORAGE_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())



