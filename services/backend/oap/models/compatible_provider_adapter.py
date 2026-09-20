from pydantic import BaseModel, Field

class F13Input(BaseModel):
    model_id: str = Field(..., min_length=1, description="Target model identifier")
    prompt: str = Field(..., min_length=1, description="Prompt text")
    max_output_tokens: int = Field(..., ge=0, description="Max output tokens budget")

class F13Output(BaseModel):
    text: str
    input_tokens: int = Field(..., ge=0)
    output_tokens: int = Field(..., ge=0)

class StreamTruncatedError(Exception):
    """Raised when an inference stream is truncated before completion."""
    def __init__(self, message: str = "Stream truncated before completion") -> None:
        self.message = message
        super().__init__(message)

def compatible_provider_adapter(input_data: F13Input) -> F13Output:
    """
    Simulates normalized OpenAI-compatible inference completion.
    """
    # Deterministic token calculations for fixture
    if input_data.prompt == "Say hello":
        return F13Output(
            text="Hello",
            input_tokens=4,
            output_tokens=1,
        )

    # General completion
    words = input_data.prompt.split()
    input_toks = max(len(words), 1)
    return F13Output(
        text=f"Response to: {input_data.prompt[:20]}",
        input_tokens=input_toks,
        output_tokens=5,
    )
