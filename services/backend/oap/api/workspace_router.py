from typing import Any, Dict
from fastapi import APIRouter, Header, status
from fastapi.responses import JSONResponse

from oap.identity.workspace_authorization import (
    F07Input,
    F07Output,
    NotFoundError,
    workspace_authorization,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/workspace", tags=["workspace"])

@router.post("/authorize", response_model=F07Output)
async def authorize_workspace(
    raw_body: Dict[str, Any],
    x_actor_workspace_id: str = Header("ws-1", alias="X-Actor-Workspace-ID"),
) -> F07Output | JSONResponse:
    if "resource_workspace_id" not in raw_body or not raw_body["resource_workspace_id"]:
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
        input_data = F07Input(**raw_body)
        return workspace_authorization(input_data, actor_workspace_id=x_actor_workspace_id)
    except NotFoundError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="NOT_FOUND",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=envelope.model_dump())
