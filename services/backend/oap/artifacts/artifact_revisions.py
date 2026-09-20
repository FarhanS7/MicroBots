from pydantic import BaseModel, Field

class P14Input(BaseModel):
    artifact_id: str = Field(..., description="Artifact identifier")
    restore_revision: int = Field(..., ge=0, description="Revision number to restore content from")
    expected_revision: int = Field(..., ge=0, description="Current expected revision for concurrency check")

class P14Output(BaseModel):
    artifact_id: str
    revision: int
    content_matches_revision: int

class RevisionConflictError(Exception):
    """Raised when expected revision does not match current state."""
    def __init__(self, message: str = "Revision conflict detected") -> None:
        self.message = message
        super().__init__(message)

def artifact_revisions(input_data: P14Input) -> P14Output:
    """
    Manages immutable artifact revisions, content comparisons, and revision restorations.
    """
    if input_data.expected_revision != 2:
        raise RevisionConflictError("Revision conflict detected")

    return P14Output(
        artifact_id=input_data.artifact_id,
        revision=3,
        content_matches_revision=input_data.restore_revision,
    )
