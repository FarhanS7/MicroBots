from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.browser.structured_browser_tools import (
    F19Input,
    F19Output,
    PrivateNetworkBlockedError,
    structured_browser_tools,
)
from oap.browser.persistent_browser_profile import (
    P11Input,
    P11Output,
    ProfileLeaseConflictError,
    persistent_browser_profile,
)
from oap.browser.browser_action_suite import (
    P12Input,
    P12Output,
    UserChallengeRequiredError,
    browser_action_suite,
)
from oap.browser.browser_file_transfer import (
    P24Input,
    P24Output,
    UnapprovedDestinationError,
    browser_file_transfer,
)
from oap.browser.browser_script_inspection import (
    P25Input,
    P25Output,
    InspectionForbiddenError,
    browser_script_inspection,
)
from oap.browser.remote_display_takeover import (
    D04Input,
    D04Output,
    LeaseConflictError,
    remote_display_takeover,
)
from oap.browser.visual_action_fallback import (
    D05Input,
    D05Output,
    StaleScreenshotError,
    visual_action_fallback,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/browser", tags=["browser"])

@router.post("/navigate", response_model=None)
async def navigate_browser(raw_body: Dict[str, Any]) -> F19Output | JSONResponse:
    if "url" not in raw_body or not raw_body["url"]:
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
        input_data = F19Input(**raw_body)
        return structured_browser_tools(input_data)
    except PrivateNetworkBlockedError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="FORBIDDEN",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=envelope.model_dump())

@router.post("/profile", response_model=None)
async def configure_browser_profile(raw_body: Dict[str, Any]) -> P11Output | JSONResponse:
    if "profile_id" not in raw_body or "persist" not in raw_body:
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
        input_data = P11Input(**raw_body)
        return persistent_browser_profile(input_data)
    except ProfileLeaseConflictError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="CONFLICT",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=envelope.model_dump())

@router.post("/action", response_model=None)
async def execute_browser_action(raw_body: Dict[str, Any]) -> P12Output | JSONResponse:
    if "page_id" not in raw_body or "action" not in raw_body or "target" not in raw_body:
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
        input_data = P12Input(**raw_body)
        return browser_action_suite(input_data)
    except UserChallengeRequiredError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="WAITING_USER",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=envelope.model_dump())

@router.post("/transfer", response_model=None)
async def transfer_browser_file(raw_body: Dict[str, Any]) -> P24Output | JSONResponse:
    required_keys = ["page_id", "action", "target"]
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
        input_data = P24Input(**raw_body)
        return browser_file_transfer(input_data)
    except UnapprovedDestinationError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="FORBIDDEN",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=envelope.model_dump())

@router.post("/inspect", response_model=None)
async def inspect_browser_script(raw_body: Dict[str, Any]) -> P25Output | JSONResponse:
    required_keys = ["page_id", "operation"]
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
        input_data = P25Input(**raw_body)
        return browser_script_inspection(input_data)
    except InspectionForbiddenError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="FORBIDDEN",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=envelope.model_dump())

@router.post("/takeover", response_model=None)
async def handle_remote_display_takeover(raw_body: Dict[str, Any]) -> D04Output | JSONResponse:
    required_keys = ["computer_id", "mode"]
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
        input_data = D04Input(**raw_body)
        return remote_display_takeover(input_data)
    except LeaseConflictError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="LEASE_CONFLICT",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=envelope.model_dump())

@router.post("/visual-fallback", response_model=None)
async def handle_visual_action_fallback(raw_body: Dict[str, Any]) -> D05Output | JSONResponse:
    required_keys = ["computer_id", "screenshot_revision", "x", "y"]
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
        input_data = D05Input(**raw_body)
        return visual_action_fallback(input_data)
    except StaleScreenshotError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="STALE_SCREENSHOT",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())


