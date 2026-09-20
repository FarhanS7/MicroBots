from typing import Any, Dict
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from oap.agents.agent_definition import F10Input, F10Output, agent_definition
from oap.agents.conversational_agent_creation import (
    I17Input,
    I17Output,
    conversational_agent_creation,
)
from oap.domain.toolchain import PublicErrorEnvelope, ErrorDetail

router = APIRouter(prefix="/api/v1/agents", tags=["agents"])

@router.post("", response_model=F10Output)
async def create_agent(raw_body: Dict[str, Any]) -> F10Output | JSONResponse:
    required_keys = ["name", "role", "instruction", "model_id"]
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

    input_data = F10Input(**raw_body)
    return agent_definition(input_data)

@router.post("/conversational", response_model=None)
async def handle_conversational_agent_creation(raw_body: Dict[str, Any]) -> I17Output | JSONResponse:
    if "description" not in raw_body or not raw_body["description"]:
        envelope = PublicErrorEnvelope(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Required input fields are missing",
                retryable=False,
            ),
            trace_id="trace-test",
        )
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=envelope.model_dump())

    input_data = I17Input(**raw_body)
    return conversational_agent_creation(input_data)

