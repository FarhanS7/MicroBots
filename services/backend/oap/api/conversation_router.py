from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.conversation.persistent_messages import (
    F11Input,
    F11Output,
    IdempotencyConflictError,
    persistent_messages,
)
from oap.conversation.attachments_rich_messages import (
    P21Input,
    P21Output,
    InvalidAttachmentError,
    attachments_rich_messages,
)
from oap.conversation.tool_skill_invocation import (
    A17Input,
    A17Output,
    UnauthorizedSkillInvocationError,
    tool_skill_invocation,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/conversation", tags=["conversation"])

@router.post("/messages", response_model=F11Output)
async def create_message(raw_body: Dict[str, Any]) -> F11Output | JSONResponse:
    required_keys = ["agent_id", "client_message_id", "text"]
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
        input_data = F11Input(**raw_body)
        return persistent_messages(input_data)
    except IdempotencyConflictError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="IDEMPOTENCY_CONFLICT",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=envelope.model_dump())

@router.post("/attachments", response_model=None)
async def create_attachment(raw_body: Dict[str, Any]) -> P21Output | JSONResponse:
    required_keys = ["conversation_id", "file_id", "media_type"]
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
        input_data = P21Input(**raw_body)
        return attachments_rich_messages(input_data)
    except InvalidAttachmentError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/tool-skill", response_model=None)
async def invoke_tool_skill(raw_body: Dict[str, Any]) -> A17Output | JSONResponse:
    required_keys = ["message_id", "skill_id", "version"]
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
        input_data = A17Input(**raw_body)
        return tool_skill_invocation(input_data)
    except UnauthorizedSkillInvocationError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())
