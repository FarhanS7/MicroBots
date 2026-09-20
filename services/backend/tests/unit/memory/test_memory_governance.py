import pytest
from oap.memory.memory_governance import (
    P09Input,
    P09Output,
    MemoryDisabledError,
    memory_governance,
    reset_memory_store,
)

def setup_function():
    reset_memory_store()

def test_unit_memory_governance_happy_path():
    inp = P09Input(category="preference", text="Use concise summaries", source_message_id="message-1")
    res = memory_governance(inp)
    assert isinstance(res, P09Output)
    assert res.memory_id == "memory-1"
    assert res.status == "user_confirmed"

def test_unit_memory_governance_disabled():
    inp = P09Input(category="preference", text="Use concise summaries", source_message_id="disabled")
    with pytest.raises(MemoryDisabledError):
        memory_governance(inp)
