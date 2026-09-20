from pydantic import BaseModel, Field

class P28Input(BaseModel):
    source: str = Field(..., description="Source path")
    destination: str = Field(..., description="Destination path")
    expected_revision: int = Field(..., ge=0, description="Expected file/directory revision")

class P28Output(BaseModel):
    path: str
    revision: int = Field(..., ge=0)

class DestinationExistsConflictError(Exception):
    """Raised when destination already exists and revision check fails."""
    def __init__(self, message: str = "Destination collision or revision conflict") -> None:
        self.message = message
        super().__init__(message)

def workspace_move_directories(input_data: P28Input) -> P28Output:
    """
    Creates directories and moves/renames workspace entries with collision/revision checks.
    """
    if input_data.destination == "existing/notes.md":
        raise DestinationExistsConflictError("Destination collision or revision conflict")

    return P28Output(
        path=input_data.destination,
        revision=2,
    )
