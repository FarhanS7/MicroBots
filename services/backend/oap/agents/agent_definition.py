from typing import Dict, Any
from pydantic import BaseModel, Field

class F10Input(BaseModel):
    name: str = Field(..., min_length=1, description="Agent display name")
    role: str = Field(..., min_length=1, description="Agent role summary")
    instruction: str = Field(..., min_length=1, description="Behavioral instructions")
    model_id: str = Field(..., min_length=1, description="Preferred model identifier")

class F10Output(BaseModel):
    agent_id: str
    state: str
    revision: int = Field(..., ge=0)

# In-memory store for agent definitions
_AGENTS_STORE: Dict[str, Dict[str, Any]] = {}
_AGENT_COUNTER: int = 0

def agent_definition(input_data: F10Input, agent_id: str | None = None) -> F10Output:
    """
    Creates or updates persistent agent identity.
    """
    global _AGENT_COUNTER

    if not agent_id:
        _AGENT_COUNTER += 1
        agent_id = f"agent-{_AGENT_COUNTER}"

    existing = _AGENTS_STORE.get(agent_id)
    revision = existing["revision"] + 1 if existing else 1
    state = existing["state"] if existing else "idle"

    record = {
        "agent_id": agent_id,
        "name": input_data.name,
        "role": input_data.role,
        "instruction": input_data.instruction,
        "model_id": input_data.model_id,
        "state": state,
        "revision": revision,
    }
    _AGENTS_STORE[agent_id] = record

    return F10Output(
        agent_id=agent_id,
        state=state,
        revision=revision,
    )

def reset_agents_store() -> None:
    global _AGENT_COUNTER
    _AGENTS_STORE.clear()
    _AGENT_COUNTER = 0
