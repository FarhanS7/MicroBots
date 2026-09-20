import pytest
from oap.memory.retention_deletion_worker import (
    P27Input,
    P27Output,
    retention_deletion_worker,
)

def test_retention_deletion_worker_happy_path():
    inp = P27Input(memory_id="memory-1", action="delete")
    out = retention_deletion_worker(inp)
    assert out.memory_deleted is True
    assert out.derived_entries_deleted is True
