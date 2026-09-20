from typing import Any, Dict
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from oap.domain.toolchain import (
    F01Input,
    F01Output,
    PrerequisiteError,
    PublicErrorEnvelope,
    ErrorDetail,
    verify_toolchain_contract,
)

router = APIRouter(prefix="/api/v1/toolchain", tags=["toolchain"])

@router.post("/verify", response_model=F01Output)
async def verify_toolchain(raw_body: Dict[str, Any]) -> F01Output | JSONResponse:
    if "environment" not in raw_body or not raw_body["environment"]:
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
        input_data = F01Input(**raw_body)
        return verify_toolchain_contract(input_data)
    except PrerequisiteError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="PREREQUISITE_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_412_PRECONDITION_FAILED, content=envelope.model_dump())
