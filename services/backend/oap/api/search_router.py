from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.search.file_global_search import (
    I13Input,
    I13Output,
    file_global_search,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/search", tags=["search"])

@router.post("/global", response_model=None)
async def handle_global_search(raw_body: Dict[str, Any]) -> I13Output | JSONResponse:
    required_keys = ["query", "types", "limit"]
    if not all(k in raw_body for k in required_keys):
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Required input fields are missing",
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

    input_data = I13Input(**raw_body)
    return file_global_search(input_data)
