from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.skills.skill_package_schema import (
    A01Input,
    A01Output,
    InvalidSkillManifestError,
    skill_package_schema,
)
from oap.skills.skill_install_version import (
    A02Input,
    A02Output,
    UnsafeArchiveError,
    skill_install_version,
)
from oap.skills.draft_skill_from_work import (
    A03Input,
    A03Output,
    draft_skill_from_work,
)
from oap.skills.demonstration_to_skill import (
    D06Input,
    D06Output,
    demonstration_to_skill,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/skills", tags=["skills"])

@router.post("/schema", response_model=None)
async def validate_skill_schema(raw_body: Dict[str, Any]) -> A01Output | JSONResponse:
    required_keys = ["name", "version", "required_tools"]
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
        input_data = A01Input(**raw_body)
        return skill_package_schema(input_data)
    except InvalidSkillManifestError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/install", response_model=None)
async def install_skill_version(raw_body: Dict[str, Any]) -> A02Output | JSONResponse:
    required_keys = ["package", "version"]
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
        input_data = A02Input(**raw_body)
        return skill_install_version(input_data)
    except UnsafeArchiveError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="FORBIDDEN",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=envelope.model_dump())

@router.post("/draft", response_model=None)
async def draft_skill(raw_body: Dict[str, Any]) -> A03Output | JSONResponse:
    required_keys = ["source_task_id", "name"]
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

    input_data = A03Input(**raw_body)
    return draft_skill_from_work(input_data)

@router.post("/demonstration", response_model=None)
async def handle_demonstration_to_skill(raw_body: Dict[str, Any]) -> D06Output | JSONResponse:
    required_keys = ["recording_id", "name"]
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

    input_data = D06Input(**raw_body)
    return demonstration_to_skill(input_data)

from oap.skills.evaluated_skill_improvement import (
    X04Input,
    X04Output,
    SkillRegressionError,
    evaluated_skill_improvement,
)

@router.post("/evaluated-improvement", response_model=None)
async def improve_evaluated_skill(raw_body: Dict[str, Any]) -> X04Output | JSONResponse:
    required_keys = ["skill_id", "candidate_version"]
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
        input_data = X04Input(**raw_body)
        return evaluated_skill_improvement(input_data)
    except SkillRegressionError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="SKILL_REGRESSION",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_412_PRECONDITION_FAILED, content=envelope.model_dump())


