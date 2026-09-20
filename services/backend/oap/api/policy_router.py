from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.policy.restricted_tool_policy import F15Input, F15Output, restricted_tool_policy
from oap.policy.approval_request import (
    P03Input,
    P03Output,
    InvalidApprovalError,
    approval_request,
)
from oap.policy.approval_consumption import (
    P04Input,
    P04Output,
    RevisionConflictError,
    approval_consumption,
)
from oap.policy.organization_policy_precedence import (
    T03Input,
    T03Output,
    organization_policy_precedence,
)
from oap.policy.trust_level_presets import (
    X09Input,
    X09Output,
    AutonomousTrustElevationForbiddenError,
    trust_level_presets,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/policy", tags=["policy"])

@router.post("/tool", response_model=F15Output)
async def evaluate_tool_policy(raw_body: Dict[str, Any]) -> F15Output | JSONResponse:
    required_keys = ["tool", "path", "policy_revision"]
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

    input_data = F15Input(**raw_body)
    return restricted_tool_policy(input_data)

@router.post("/approval", response_model=None)
async def request_action_approval(raw_body: Dict[str, Any]) -> P03Output | JSONResponse:
    required_keys = ["task_id", "action", "target", "expires_in_seconds"]
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
        input_data = P03Input(**raw_body)
        return approval_request(input_data)
    except InvalidApprovalError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/consume", response_model=None)
async def consume_action_approval(raw_body: Dict[str, Any]) -> P04Output | JSONResponse:
    required_keys = ["approval_id", "decision", "expected_revision"]
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
        input_data = P04Input(**raw_body)
        return approval_consumption(input_data)
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

@router.post("/precedence", response_model=None)
async def handle_policy_precedence(raw_body: Dict[str, Any]) -> T03Output | JSONResponse:
    required_keys = ["organization_decision", "user_decision"]
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

    input_data = T03Input(**raw_body)
    return organization_policy_precedence(input_data)


@router.post("/trust-presets", response_model=None)
async def handle_trust_level_presets(raw_body: Dict[str, Any]) -> X09Output | JSONResponse:
    required_keys = ["agent_id", "trust_level"]
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
        input_data = X09Input(**raw_body)
        return trust_level_presets(input_data)
    except AutonomousTrustElevationForbiddenError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="AUTONOMOUS_ELEVATION_FORBIDDEN",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())




