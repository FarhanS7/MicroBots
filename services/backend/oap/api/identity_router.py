from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.identity.local_owner_session import (
    F06Input,
    F06Output,
    RevisionConflictError,
    local_owner_session,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/identity", tags=["identity"])

@router.post("/session", response_model=F06Output)
async def create_session(raw_body: Dict[str, Any]) -> F06Output | JSONResponse:
    if "email" not in raw_body or "password" not in raw_body or not raw_body["email"] or not raw_body["password"]:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Required input fields are missing",
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

    input_data = F06Input(**raw_body)
    return local_owner_session(input_data, is_setup=False)

@router.post("/setup", response_model=F06Output)
async def setup_owner(raw_body: Dict[str, Any]) -> F06Output | JSONResponse:
    if "email" not in raw_body or "password" not in raw_body or not raw_body["email"] or not raw_body["password"]:
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
        input_data = F06Input(**raw_body)
        return local_owner_session(input_data, is_setup=True)
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

from oap.identity.enterprise_oidc import (
    O06Input,
    O06Output,
    OidcAuthenticationError,
    enterprise_oidc,
)

@router.post("/oidc", response_model=None)
async def authenticate_oidc(raw_body: Dict[str, Any]) -> O06Output | JSONResponse:
    required_keys = ["issuer", "subject"]
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
        input_data = O06Input(**raw_body)
        return enterprise_oidc(input_data)
    except OidcAuthenticationError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="UNAUTHENTICATED",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=envelope.model_dump())

