from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.secrets.credential_vault import (
    F08Input,
    F08Output,
    ForbiddenSecretError,
    credential_vault,
    resolve_credential,
    revoke_credential,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/secrets", tags=["secrets"])

@router.post("/vault", response_model=F08Output)
async def store_secret(raw_body: Dict[str, Any]) -> F08Output | JSONResponse:
    if "provider" not in raw_body or "credential" not in raw_body or not raw_body["provider"] or not raw_body["credential"]:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Required input fields are missing",
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

    input_data = F08Input(**raw_body)
    return credential_vault(input_data)

@router.post("/resolve", response_model=None)
async def resolve_secret(raw_body: Dict[str, Any]) -> Any:

    secret_id = raw_body.get("secret_id")
    if not secret_id:
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
        cred = resolve_credential(secret_id)
        return {"credential": cred}
    except ForbiddenSecretError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="FORBIDDEN",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=envelope.model_dump())
