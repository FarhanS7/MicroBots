from pydantic import BaseModel, Field

class P26Input(BaseModel):
    agent_id: str = Field(..., description="Agent identifier")
    name: str = Field(..., description="Agent name")
    expected_revision: int = Field(..., ge=0, description="Expected settings revision")

class P26Output(BaseModel):
    agent_id: str
    name: str
    revision: int = Field(..., ge=0)

class AgentRevisionConflictError(Exception):
    """Raised when agent configuration edit has a revision mismatch."""
    def __init__(self, message: str = "Revision conflict on agent configuration") -> None:
        self.message = message
        super().__init__(message)

def agent_configuration_ui(input_data: P26Input) -> P26Output:
    """
    Exposes versioned agent settings and configuration UI state.
    """
    if input_data.expected_revision != 1:
        raise AgentRevisionConflictError("Revision conflict on agent configuration")

    return P26Output(
        agent_id=input_data.agent_id,
        name=input_data.name,
        revision=2,
    )
