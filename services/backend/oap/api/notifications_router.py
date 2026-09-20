from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.notifications.notification_inbox import (
    A11Input,
    A11Output,
    notification_inbox,
)
from oap.notifications.email_webhook_delivery import (
    A12Input,
    A12Output,
    InvalidDeliveryDestinationError,
    email_webhook_delivery,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])

@router.post("/inbox", response_model=None)
async def create_notification(raw_body: Dict[str, Any]) -> A11Output | JSONResponse:
    required_keys = ["event_id", "kind"]
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

    input_data = A11Input(**raw_body)
    return notification_inbox(input_data)

@router.post("/delivery", response_model=None)
async def deliver_notification(raw_body: Dict[str, Any]) -> A12Output | JSONResponse:
    required_keys = ["notification_id", "channel", "destination_id"]
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
        input_data = A12Input(**raw_body)
        return email_webhook_delivery(input_data)
    except InvalidDeliveryDestinationError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())
