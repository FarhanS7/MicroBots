from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.domain.ci import F05Input, F05Output, ci_quality_gates
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/ci", tags=["ci"])

@router.post("/verify", response_model=F05Output)
async def verify_ci(raw_body: Dict[str, Any]) -> F05Output | JSONResponse:
    if "event" not in raw_body or "fork" not in raw_body or not raw_body["event"]:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Required input fields are missing",
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

    input_data = F05Input(**raw_body)
    return ci_quality_gates(input_data)
