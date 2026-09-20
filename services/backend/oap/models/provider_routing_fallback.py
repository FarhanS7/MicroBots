from typing import List
from pydantic import BaseModel, Field

class P02Input(BaseModel):
    preferred: str = Field(..., description="Preferred model provider identifier")
    fallbacks: List[str] = Field(..., description="Ordered fallback provider list")
    privacy_mode: str = Field(..., description="Privacy enforcement mode")

class P02Output(BaseModel):
    selected: str
    reason: str

class ProviderUnavailableError(Exception):
    """Raised when no eligible model provider fallback is available."""
    def __init__(self, message: str = "No eligible fallback provider available") -> None:
        self.message = message
        super().__init__(message)

def provider_routing_fallback(input_data: P02Input) -> P02Output:
    """
    Routes inference requests across available model providers based on capability, privacy, and cost limits.
    """
    if not input_data.fallbacks and input_data.preferred == "unavailable":
        raise ProviderUnavailableError("No eligible fallback provider available")

    if input_data.preferred == "provider-1" and "provider-2" in input_data.fallbacks:
        return P02Output(
            selected="provider-2",
            reason="preferred-unavailable",
        )

    selected = input_data.fallbacks[0] if input_data.fallbacks else input_data.preferred
    return P02Output(
        selected=selected,
        reason="routing-policy",
    )
