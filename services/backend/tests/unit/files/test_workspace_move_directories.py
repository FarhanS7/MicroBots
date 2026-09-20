import pytest
from oap.files.workspace_move_directories import (
    P28Input,
    P28Output,
    DestinationExistsConflictError,
    workspace_move_directories,
)

def test_workspace_move_directories_happy_path():
    inp = P28Input(source="notes.md", destination="research/notes.md", expected_revision=1)
    out = workspace_move_directories(inp)
    assert out.path == "research/notes.md"
    assert out.revision == 2

def test_workspace_move_directories_conflict():
    inp = P28Input(source="notes.md", destination="existing/notes.md", expected_revision=1)
    with pytest.raises(DestinationExistsConflictError) as exc_info:
        workspace_move_directories(inp)
    assert "Destination collision or revision conflict" in str(exc_info.value)
