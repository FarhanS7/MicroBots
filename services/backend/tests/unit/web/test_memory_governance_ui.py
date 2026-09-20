import pytest
from oap.web.memory_governance_ui import (
    P13Input,
    P13Output,
    StaleMemoryError,
    memory_governance_ui,
)

def test_memory_governance_ui_happy_path():
    inp = P13Input(panel="memory", delete_memory_id="memory-1")
    out = memory_governance_ui(inp)
    assert out.visible_memory_ids == []
    assert out.deletion_confirmed is True

def test_memory_governance_ui_stale_conflict():
    inp = P13Input(panel="memory", delete_memory_id="stale-1")
    with pytest.raises(StaleMemoryError) as exc_info:
        memory_governance_ui(inp)
    assert "Stale memory edit conflict" in str(exc_info.value)
