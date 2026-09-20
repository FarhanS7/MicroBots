from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.domain.git_community_bootstrap import (
    F02Input,
    F02Output,
    verify_git_community_bootstrap,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/bootstrap", tags=["bootstrap"])


@router.post("/verify", response_model=F02Output)
async def verify_bootstrap(raw_body: Dict[str, Any]) -> F02Output | JSONResponse:
    required_keys = ["repository", "visibility"]
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

    input_data = F02Input(**raw_body)
    return verify_git_community_bootstrap(input_data)
