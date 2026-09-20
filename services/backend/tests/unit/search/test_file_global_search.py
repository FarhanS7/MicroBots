import pytest
from oap.search.file_global_search import (
    I13Input,
    I13Output,
    file_global_search,
)

def test_file_global_search_happy_path():
    inp = I13Input(query="research", types=["file", "agent"], limit=10)
    res = file_global_search(inp)
    assert res.result_ids == ["file-1", "agent-1"]
    assert res.next_cursor is None

def test_file_global_search_filters_deleted_and_unauthorized():
    inp = I13Input(query="research", types=["file", "agent"], limit=10)
    res = file_global_search(inp)
    assert "file-deleted" not in res.result_ids
    assert "agent-unauth" not in res.result_ids
