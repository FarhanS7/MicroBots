from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.connectors.connector_registry import (
    I01Input,
    I01Output,
    InvalidConnectorAuthError,
    connector_registry,
)
from oap.connectors.mcp_client import (
    I02Input,
    I02Output,
    MCPSchemaMismatchError,
    mcp_client,
)
from oap.connectors.openapi_import import (
    I03Input,
    I03Output,
    OpenAPIImportError,
    openapi_import,
)
from oap.connectors.generic_http_auth import (
    I04Input,
    I04Output,
    HeaderStrippingRedirectError,
    generic_http_auth,
)
from oap.connectors.oauth_lifecycle import (
    I05Input,
    I05Output,
    InvalidOAuthStateError,
    oauth_lifecycle,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/connectors", tags=["connectors"])

@router.post("/registry", response_model=None)
async def register_connector(raw_body: Dict[str, Any]) -> I01Output | JSONResponse:
    required_keys = ["name", "auth_type", "secret_id"]
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
        input_data = I01Input(**raw_body)
        return connector_registry(input_data)
    except InvalidConnectorAuthError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/mcp", response_model=None)
async def call_mcp_client(raw_body: Dict[str, Any]) -> I02Output | JSONResponse:
    required_keys = ["server_id", "tool", "arguments"]
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
        input_data = I02Input(**raw_body)
        return mcp_client(input_data)
    except MCPSchemaMismatchError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/openapi", response_model=None)
async def import_openapi(raw_body: Dict[str, Any]) -> I03Output | JSONResponse:
    required_keys = ["spec_id", "operation_ids"]
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
        input_data = I03Input(**raw_body)
        return openapi_import(input_data)
    except OpenAPIImportError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/http", response_model=None)
async def execute_generic_http(raw_body: Dict[str, Any]) -> I04Output | JSONResponse:
    required_keys = ["connector_id", "method", "path"]
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
        input_data = I04Input(**raw_body)
        return generic_http_auth(input_data)
    except HeaderStrippingRedirectError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/oauth", response_model=None)
async def handle_oauth_lifecycle(raw_body: Dict[str, Any]) -> I05Output | JSONResponse:
    required_keys = ["connector_id", "callback_state", "code"]
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
        input_data = I05Input(**raw_body)
        return oauth_lifecycle(input_data)
    except InvalidOAuthStateError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())
