import pytest
from oap.web.agent_chat_ui import (
    F23Input,
    F23Output,
    TaskSubmissionError,
    agent_chat_ui,
)

def test_unit_agent_chat_ui_happy_path():
    inp = F23Input(agent_id="agent-1", instruction="Research three competitors")
    res = agent_chat_ui(inp)
    assert isinstance(res, F23Output)
    assert res.visible_task_id == "task-1"
    assert res.visible_state == "queued"

def test_unit_agent_chat_ui_submission_error():
    inp = F23Input(agent_id="agent-1", instruction="fail")
    with pytest.raises(TaskSubmissionError):
        agent_chat_ui(inp)
