import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from oap.agents.agent_definition import (
    F10Input,
    F10Output,
    agent_definition,
    reset_agents_store,
)

def setup_function() -> None:
    reset_agents_store()

def test_unit_agent_definition_happy_path() -> None:
    inp = F10Input(
        name="Researcher",
        role="Research",
        instruction="Produce cited reports",
        model_id="model-1",
    )
    out = agent_definition(inp)
    assert out == F10Output(agent_id="agent-1", state="idle", revision=1)
