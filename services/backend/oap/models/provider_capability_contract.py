from typing import List, Dict, Set
from pydantic import BaseModel, Field

class F12Input(BaseModel):
    provider_id: str = Field(..., description="Target model provider ID")
    required_capabilities: List[str] = Field(..., description="List of required capabilities e.g. tools, vision")

class F12Output(BaseModel):
    compatible: bool
    provider_id: str

class CapabilityUnsupportedError(Exception):
    """Raised when requested capabilities are unsupported by the provider."""
    def __init__(self, message: str = "Requested capabilities are unsupported by provider") -> None:
        self.message = message
        super().__init__(message)

# Registry of supported capabilities per provider
_PROVIDER_CAPABILITIES: Dict[str, Set[str]] = {
    "provider-1": {"text", "tools", "vision", "streaming"},
    "text-only-provider": {"text", "streaming"},
}

def provider_capability_contract(input_data: F12Input) -> F12Output:
    """
    Validates required capabilities against provider capability registry.
    """
    supported = _PROVIDER_CAPABILITIES.get(input_data.provider_id, {"text", "tools", "vision", "streaming"})
    
    missing = set(input_data.required_capabilities) - supported
    if missing:
        raise CapabilityUnsupportedError(f"Capabilities unsupported by provider: {list(missing)}")

    return F12Output(
        compatible=True,
        provider_id=input_data.provider_id,
    )
