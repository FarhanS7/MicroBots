import pytest
from oap.templates.agent_portability import (
    I12Input,
    I12Output,
    agent_portability,
)

def test_agent_portability_happy_path():
    inp = I12Input(agent_id="agent-1", include_private_data=False)
    res = agent_portability(inp)
    assert res.template_id == "template-1"
    assert res.secrets_included is False
    assert res.history_included is False

def test_agent_portability_missing_plugin():
    inp = I12Input(agent_id="missing_plugin_agent", include_private_data=False)
    res = agent_portability(inp)
    assert res.template_id == "template-1"
    assert res.unresolved_dependencies == ["plugin-missing-1"]
