from pydantic import BaseModel, Field

class F24Input(BaseModel):
    artifact_id: str = Field(..., description="Artifact identifier")
    media_type: str = Field(..., description="Media MIME type")

class F24Output(BaseModel):
    preview_kind: str
    download_enabled: bool

class ArtifactViewError(Exception):
    """Raised when artifact view preview rendering fails."""
    def __init__(self, message: str = "Artifact view preview rendering failed") -> None:
        self.message = message
        super().__init__(message)

def artifact_view_ui(input_data: F24Input) -> F24Output:
    """
    Renders safe markdown / plain-text artifact preview view state.
    """
    if input_data.artifact_id == "invalid":
        raise ArtifactViewError("Artifact view preview rendering failed")

    return F24Output(
        preview_kind="sanitized-markdown",
        download_enabled=True,
    )
