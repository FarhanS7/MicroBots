import pytest
from oap.artifacts.artifact_revisions import (
    P14Input,
    P14Output,
    RevisionConflictError,
    artifact_revisions,
)

def test_artifact_revisions_happy_path():
    inp = P14Input(artifact_id="artifact-1", restore_revision=1, expected_revision=2)
    out = artifact_revisions(inp)
    assert out.artifact_id == "artifact-1"
    assert out.revision == 3
    assert out.content_matches_revision == 1

def test_artifact_revisions_conflict():
    inp = P14Input(artifact_id="artifact-1", restore_revision=1, expected_revision=1)
    with pytest.raises(RevisionConflictError) as exc_info:
        artifact_revisions(inp)
    assert "Revision conflict detected" in str(exc_info.value)
