import pytest
from oap.files.workspace_file_operations import (
    F17Input,
    F17Output,
    TraversalError,
    workspace_file_operations,
    reset_file_store,
)

def setup_function():
    reset_file_store()

def test_unit_workspace_file_operations_happy_path():
    inp = F17Input(
        path="report.md",
        content="# Research",
        expected_revision=0,
    )
    res = workspace_file_operations(inp)
    assert isinstance(res, F17Output)
    assert res.path == "report.md"
    assert res.revision == 1
    assert res.bytes == 10

def test_unit_workspace_file_operations_traversal_forbidden():
    inp = F17Input(
        path="../etc/passwd",
        content="root",
        expected_revision=0,
    )
    with pytest.raises(TraversalError):
        workspace_file_operations(inp)
