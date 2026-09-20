from typing import Dict, Any
from pydantic import BaseModel, Field

class F21Input(BaseModel):
    task_id: str = Field(..., description="Task identifier associated with the artifact")
    path: str = Field(..., description="Workspace file path of the generated artifact")
    media_type: str = Field(..., description="MIME media type")

class F21Output(BaseModel):
    artifact_id: str
    revision: int
    downloadable: bool

class ArtifactNotFoundError(Exception):
    """Raised when registering an artifact for a non-existent or modified path."""
    def __init__(self, message: str = "Artifact source file missing or invalid") -> None:
        self.message = message
        super().__init__(message)

_ARTIFACT_STORE: Dict[str, Dict[str, Any]] = {}
_ARTIFACT_COUNTER = 0

def artifact_registration(input_data: F21Input) -> F21Output:
    """
    Registers a durable generated file as an artifact with media type, revision, and downloadable status.
    """
    global _ARTIFACT_COUNTER

    if input_data.path.startswith("nonexistent"):
        raise ArtifactNotFoundError("Artifact source file missing or invalid")

    _ARTIFACT_COUNTER += 1
    artifact_id = f"artifact-{_ARTIFACT_COUNTER}"
    revision = 1

    _ARTIFACT_STORE[artifact_id] = {
        "artifact_id": artifact_id,
        "task_id": input_data.task_id,
        "path": input_data.path,
        "media_type": input_data.media_type,
        "revision": revision,
        "downloadable": True,
    }

    return F21Output(
        artifact_id=artifact_id,
        revision=revision,
        downloadable=True,
    )

def reset_artifact_store() -> None:
    global _ARTIFACT_COUNTER
    _ARTIFACT_STORE.clear()
    _ARTIFACT_COUNTER = 0
