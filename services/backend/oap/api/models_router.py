from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.models.provider_capability_contract import (
    F12Input,
    F12Output,
    CapabilityUnsupportedError,
    provider_capability_contract,
)
from oap.models.compatible_provider_adapter import (
    F13Input,
    F13Output,
    StreamTruncatedError,
    compatible_provider_adapter,
)
from oap.models.local_inference_adapter import (
    P01Input,
    P01Output,
    LocalModelUnavailableError,
    local_inference_adapter,
)
from oap.models.provider_routing_fallback import (
    P02Input,
    P02Output,
    ProviderUnavailableError,
    provider_routing_fallback,
)
from oap.models.anthropic_adapter import (
    P16Input,
    P16Output,
    AdapterConformanceError,
    anthropic_adapter,
)
from oap.models.google_adapter import (
    P17Input,
    P17Output,
    GoogleCapabilityUnsupportedError,
    google_adapter,
)
from oap.models.xai_adapter import (
    P18Input,
    P18Output,
    XaiRateLimitError,
    xai_adapter,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/models", tags=["models"])

@router.post("/capability", response_model=F12Output)
async def check_capability(raw_body: Dict[str, Any]) -> F12Output | JSONResponse:
    if "provider_id" not in raw_body or "required_capabilities" not in raw_body:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Required input fields are missing",
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

    if not raw_body["provider_id"] or not isinstance(raw_body["required_capabilities"], list):
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
        input_data = F12Input(**raw_body)
        return provider_capability_contract(input_data)
    except CapabilityUnsupportedError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="CAPABILITY_UNSUPPORTED",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=envelope.model_dump())

@router.post("/generate", response_model=F13Output)
async def generate_completion(raw_body: Dict[str, Any]) -> F13Output | JSONResponse:
    required_keys = ["model_id", "prompt", "max_output_tokens"]
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
        input_data = F13Input(**raw_body)
        return compatible_provider_adapter(input_data)
    except StreamTruncatedError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="STREAM_TRUNCATED_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=envelope.model_dump())

@router.post("/local", response_model=None)
async def handle_local_inference(raw_body: Dict[str, Any]) -> P01Output | JSONResponse:
    required_keys = ["endpoint", "privacy_mode"]
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
        input_data = P01Input(**raw_body)
        return local_inference_adapter(input_data)
    except LocalModelUnavailableError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="SERVICE_UNAVAILABLE",
                message=str(exc),
                retryable=True,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=envelope.model_dump())

@router.post("/route", response_model=None)
async def handle_provider_routing(raw_body: Dict[str, Any]) -> P02Output | JSONResponse:
    required_keys = ["preferred", "fallbacks", "privacy_mode"]
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
        input_data = P02Input(**raw_body)
        return provider_routing_fallback(input_data)
    except ProviderUnavailableError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="PROVIDER_UNAVAILABLE",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=envelope.model_dump())

@router.post("/anthropic", response_model=None)
async def handle_anthropic_adapter(raw_body: Dict[str, Any]) -> P16Output | JSONResponse:
    required_keys = ["provider", "required_capabilities"]
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
        input_data = P16Input(**raw_body)
        return anthropic_adapter(input_data)
    except AdapterConformanceError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="UNSUPPORTED",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/google", response_model=None)
async def handle_google_adapter(raw_body: Dict[str, Any]) -> P17Output | JSONResponse:
    required_keys = ["provider", "required_capabilities"]
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
        input_data = P17Input(**raw_body)
        return google_adapter(input_data)
    except GoogleCapabilityUnsupportedError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="CAPABILITY_UNSUPPORTED",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=envelope.model_dump())

@router.post("/xai", response_model=None)
async def handle_xai_adapter(raw_body: Dict[str, Any]) -> P18Output | JSONResponse:
    required_keys = ["provider", "required_capabilities"]
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
        input_data = P18Input(**raw_body)
        return xai_adapter(input_data)
    except XaiRateLimitError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="RATE_LIMITED",
                message=str(exc),
                retryable=True,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS, content=envelope.model_dump())
