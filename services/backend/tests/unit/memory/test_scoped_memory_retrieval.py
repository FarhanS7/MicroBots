import pytest
from oap.memory.scoped_memory_retrieval import (
    P10Input,
    P10Output,
    MemoryRetrievalError,
    scoped_memory_retrieval,
)

def test_unit_scoped_memory_retrieval_happy_path():
    inp = P10Input(query="summary style", limit=3)
    res = scoped_memory_retrieval(inp)
    assert isinstance(res, P10Output)
    assert res.memory_ids == ["memory-1"]
    assert res.truncated is False

def test_unit_scoped_memory_retrieval_error():
    inp = P10Input(query="invalid", limit=3)
    with pytest.raises(MemoryRetrievalError):
        scoped_memory_retrieval(inp)
