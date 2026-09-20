from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.workflows.workflow_definition import (
    A04Input,
    A04Output,
    UnboundedCycleError,
    workflow_definition,
)
from oap.workflows.hybrid_workflow_runner import (
    A05Input,
    A05Output,
    hybrid_workflow_runner,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/workflows", tags=["workflows"])

@router.post("/definition", response_model=None)
async def validate_workflow_definition(raw_body: Dict[str, Any]) -> A04Output | JSONResponse:
    required_keys = ["nodes", "edges"]
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
        input_data = A04Input(**raw_body)
        return workflow_definition(input_data)
    except UnboundedCycleError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

@router.post("/run", response_model=None)
async def execute_hybrid_workflow(raw_body: Dict[str, Any]) -> A05Output | JSONResponse:
    required_keys = ["workflow_id", "version", "input"]
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

    input_data = A05Input(**raw_body)
    return hybrid_workflow_runner(input_data)

from oap.workflows.workflow_compilation import (
    X06Input,
    X06Output,
    EquivalenceUnprovenError,
    workflow_compilation,
)

@router.post("/compilation", response_model=None)
async def compile_workflow(raw_body: Dict[str, Any]) -> X06Output | JSONResponse:
    required_keys = ["workflow_id", "target"]
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
        input_data = X06Input(**raw_body)
        return workflow_compilation(input_data)
    except EquivalenceUnprovenError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="EQUIVALENCE_UNPROVEN",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_412_PRECONDITION_FAILED, content=envelope.model_dump())

from oap.workflows.adaptive_workflow_optimization import (
    X10Input,
    X10Output,
    OptimizationRejectedError,
    adaptive_workflow_optimization,
)

@router.post("/optimize", response_model=None)
async def optimize_workflow(raw_body: Dict[str, Any]) -> X10Output | JSONResponse:
    required_keys = ["workflow_id", "objective"]
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
        input_data = X10Input(**raw_body)
        return adaptive_workflow_optimization(input_data)
    except OptimizationRejectedError as exc:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="OPTIMIZATION_REJECTED",
                message=str(exc),
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())


