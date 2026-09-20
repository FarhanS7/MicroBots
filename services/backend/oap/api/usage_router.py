from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.usage.budget_reservations import (
    P08Input,
    P08Output,
    BudgetExceededError,
    budget_reservations,
)
from oap.usage.organization_quotas import (
    T06Input,
    T06Output,
    QuotaExceededError,
    organization_quotas,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/usage", tags=["usage"])

@router.post("/reserve", response_model=None)
async def reserve_budget(raw_body: Dict[str, Any]) -> P08Output | JSONResponse:
    required_keys = ["budget_micro_usd", "reserved_micro_usd", "requested_micro_usd"]
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
        input_data = P08Input(**raw_body)
        return budget_reservations(input_data)
    except BudgetExceededError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="BUDGET_EXCEEDED",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/quotas/reserve", response_model=None)
async def reserve_organization_quota(raw_body: Dict[str, Any]) -> T06Output | JSONResponse:
    required_keys = ["organization_id", "limit_micro_usd", "requested_micro_usd"]
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
        input_data = T06Input(**raw_body)
        return organization_quotas(input_data)
    except QuotaExceededError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="QUOTA_EXCEEDED",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

