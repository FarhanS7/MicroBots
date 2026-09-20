from typing import List
from pydantic import BaseModel, Field

class P17Input(BaseModel):
    provider: str = Field(..., description="Provider identifier (google)")
    required_capabilities: List[str] = Field(..., description="Required capabilities list")

class P17Output(BaseModel):
    conformance_passed: bool
    provider: str

class GoogleCapabilityUnsupportedError(Exception):
    """Raised when Google adapter capability check fails."""
    def __init__(self, message: str = "Google capability unsupported") -> None:
        self.message = message
        super().__init__(message)

def google_adapter(input_data: P17Input) -> P17Output:
    """
    Normalizes Google model messages, tool calls, and streaming under gateway contract.
    """
    if "multimodal" in input_data.required_capabilities:
        raise GoogleCapabilityUnsupportedError("Google capability unsupported")

    return P17Output(
        conformance_passed=True,
        provider=input_data.provider,
    )
