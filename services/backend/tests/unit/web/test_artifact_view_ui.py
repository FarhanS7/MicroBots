import pytest
from oap.web.artifact_view_ui import (
    F24Input,
    F24Output,
    ArtifactViewError,
    artifact_view_ui,
)

def test_unit_artifact_view_ui_happy_path():
    inp = F24Input(artifact_id="artifact-1", media_type="text/markdown")
    res = artifact_view_ui(inp)
    assert isinstance(res, F24Output)
    assert res.preview_kind == "sanitized-markdown"
    assert res.download_enabled is True

def test_unit_artifact_view_ui_error():
    inp = F24Input(artifact_id="invalid", media_type="text/markdown")
    with pytest.raises(ArtifactViewError):
        artifact_view_ui(inp)
