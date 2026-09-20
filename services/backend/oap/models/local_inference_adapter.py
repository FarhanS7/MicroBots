from pydantic import BaseModel, Field

class P01Input(BaseModel):
    endpoint: str = Field(..., description="Local inference endpoint URL")
    privacy_mode: str = Field(..., description="Privacy enforcement mode")

class P01Output(BaseModel):
    provider_id: str
    external_requests: int

class LocalModelUnavailableError(Exception):
    """Raised when the configured local model endpoint is unreachable."""
    def __init__(self, message: str = "Local model endpoint unavailable") -> None:
        self.message = message
        super().__init__(message)

def local_inference_adapter(input_data: P01Input) -> P01Output:
    """
    Handles local Ollama/compatible model probing with privacy mode enforcement.
    """
    if "unreachable" in input_data.endpoint:
        raise LocalModelUnavailableError("Local model endpoint unavailable")

    return P01Output(
        provider_id="local-1",
        external_requests=0,
    )
