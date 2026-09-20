import pytest
from oap.web.agent_configuration_ui import (
    P26Input,
    P26Output,
    AgentRevisionConflictError,
    agent_configuration_ui,
)

def test_agent_configuration_ui_happy_path():
    inp = P26Input(agent_id="agent-1", name="Scout", expected_revision=1)
    out = agent_configuration_ui(inp)
    assert out.agent_id == "agent-1"
    assert out.name == "Scout"
    assert out.revision == 2

def test_agent_configuration_ui_conflict():
    inp = P26Input(agent_id="agent-1", name="Scout", expected_revision=2)
    with pytest.raises(AgentRevisionConflictError) as exc_info:
        agent_configuration_ui(inp)
    assert "Revision conflict on agent configuration" in str(exc_info.value)
