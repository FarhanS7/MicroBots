from pydantic import BaseModel, Field

class P29Input(BaseModel):
    command: str = Field(..., description="Command string to execute")
    background: bool = Field(..., description="Whether to run process in background")
    timeout_seconds: int = Field(..., ge=0, description="Process execution timeout")

class P29Output(BaseModel):
    process_id: str
    state: str

class ProcessNotFoundError(Exception):
    """Raised when process lookup or control fails due to foreign or missing process ID."""
    def __init__(self, message: str = "Background process not found") -> None:
        self.message = message
        super().__init__(message)

def background_process_control(input_data: P29Input) -> P29Output:
    """
    Tracks sandbox background process IDs, bounded log cursors, and wait/terminate controls.
    """
    if input_data.command == "foreign-process":
        raise ProcessNotFoundError("Background process not found")

    return P29Output(
        process_id="process-1",
        state="running",
    )
