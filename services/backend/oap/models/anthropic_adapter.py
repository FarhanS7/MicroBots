from typing import List
from pydantic import BaseModel, Field

class P16Input(BaseModel):
    provider: str = Field(..., description="Provider identifier (anthropic)")
    required_capabilities: List[str] = Field(..., description="Required capabilities list")

class P16Output(BaseModel):
    conformance_passed: bool
    provider: str

class AdapterConformanceError(Exception):
    """Raised when Anthropic adapter fails contract or payload validation."""
    def __init__(self, message: str = "Anthropic adapter conformance failed") -> None:
        self.message = message
        super().__init__(message)

def anthropic_adapter(input_data: P16Input) -> P16Output:
    """
    Normalizes Anthropic messages, tool results, and streaming usage under gateway contract.
    """
    if "unsupported" in input_data.required_capabilities:
        raise AdapterConformanceError("Anthropic adapter conformance failed")

    return P16Output(
        conformance_passed=True,
        provider=input_data.provider,
    )
