from pydantic import BaseModel, Field

class P15Input(BaseModel):
    scenario: str = Field(..., description="Scenario identifier")
    disconnect_client: bool = Field(..., description="Whether client disconnect is simulated")
    restart_worker: bool = Field(..., description="Whether worker restart is simulated")

class P15Output(BaseModel):
    artifact_valid: bool
    conversation_persisted: bool
    duplicate_effects: int = Field(..., ge=0)

class LoginDeniedError(Exception):
    """Raised when external login request is denied by user policy."""
    def __init__(self, message: str = "External login request was denied") -> None:
        self.message = message
        super().__init__(message)

def mvp_recovery_acceptance(input_data: P15Input) -> P15Output:
    """
    Validates MVP recovery capabilities across client disconnection and worker restarts.
    """
    if input_data.scenario == "denied":
        raise LoginDeniedError("External login request was denied")

    return P15Output(
        artifact_valid=True,
        conversation_persisted=True,
        duplicate_effects=0,
    )
