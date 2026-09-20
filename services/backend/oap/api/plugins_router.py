from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.plugins.plugin_manifest_runtime import (
    I06Input,
    I06Output,
    PluginPermissionDeniedError,
    plugin_manifest_runtime,
)
from oap.plugins.typescript_sdk import (
    I07Input,
    I07Output,
    IncompatibleProtocolError,
    typescript_sdk,
)
from oap.plugins.python_sdk import (
    I08Input,
    I08Output,
    SDKPayloadMismatchError,
    python_sdk,
)
from oap.plugins.plugin_event_ui_extension import (
    I09Input,
    I09Output,
    PluginScopeViolationError,
    plugin_event_ui_extension,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/plugins", tags=["plugins"])

@router.post("/manifest", response_model=None)
async def validate_plugin_manifest(raw_body: Dict[str, Any]) -> I06Output | JSONResponse:
    required_keys = ["name", "version", "permissions"]
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
        input_data = I06Input(**raw_body)
        return plugin_manifest_runtime(input_data)
    except PluginPermissionDeniedError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/ts-sdk", response_model=None)
async def validate_typescript_sdk(raw_body: Dict[str, Any]) -> I07Output | JSONResponse:
    required_keys = ["sdk_language", "fixture"]
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
        input_data = I07Input(**raw_body)
        return typescript_sdk(input_data)
    except IncompatibleProtocolError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/python-sdk", response_model=None)
async def validate_python_sdk(raw_body: Dict[str, Any]) -> I08Output | JSONResponse:
    required_keys = ["sdk_language", "fixture"]
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
        input_data = I08Input(**raw_body)
        return python_sdk(input_data)
    except SDKPayloadMismatchError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/events", response_model=None)
async def subscribe_plugin_events(raw_body: Dict[str, Any]) -> I09Output | JSONResponse:
    required_keys = ["plugin_id", "event_type"]
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
        input_data = I09Input(**raw_body)
        return plugin_event_ui_extension(input_data)
    except PluginScopeViolationError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())
