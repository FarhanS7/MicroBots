import pytest
from oap.artifacts.artifact_registration import (
    F21Input,
    F21Output,
    ArtifactNotFoundError,
    artifact_registration,
    reset_artifact_store,
)

def setup_function():
    reset_artifact_store()

def test_unit_artifact_registration_happy_path():
    inp = F21Input(
        task_id="task-1",
        path="report.md",
        media_type="text/markdown",
    )
    res = artifact_registration(inp)
    assert isinstance(res, F21Output)
    assert res.artifact_id == "artifact-1"
    assert res.revision == 1
    assert res.downloadable is True

def test_unit_artifact_registration_missing_file():
    inp = F21Input(
        task_id="task-1",
        path="nonexistent_file.png",
        media_type="image/png",
    )
    with pytest.raises(ArtifactNotFoundError):
        artifact_registration(inp)
