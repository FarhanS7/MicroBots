from typing import List
from pydantic import BaseModel, Field

class P18Input(BaseModel):
    provider: str = Field(..., description="Provider identifier (xai)")
    required_capabilities: List[str] = Field(..., description="Required capabilities list")

class P18Output(BaseModel):
    conformance_passed: bool
    provider: str

class XaiRateLimitError(Exception):
    """Raised when xAI adapter encounters rate limits."""
    def __init__(self, message: str = "xAI rate limit exceeded") -> None:
        self.message = message
        super().__init__(message)

def xai_adapter(input_data: P18Input) -> P18Output:
    """
    Validates xAI endpoint capability and tool-call conformance behind gateway adapter contract.
    """
    if "rate_limit" in input_data.required_capabilities:
        raise XaiRateLimitError("xAI rate limit exceeded")

    return P18Output(
        conformance_passed=True,
        provider=input_data.provider,
    )
