import pytest
from oap.conversation.tool_skill_invocation import (
    A17Input,
    UnauthorizedSkillInvocationError,
    tool_skill_invocation,
)

def test_tool_skill_invocation_happy_path():
    inp = A17Input(
        message_id="message-1",
        skill_id="skill-1",
        version="1.0.0"
    )
    res = tool_skill_invocation(inp)
    assert res.invocation_id == "invocation-1"
    assert res.permission_widened is False

def test_tool_skill_invocation_unauthorized():
    inp = A17Input(
        message_id="message-1",
        skill_id="unauthorized-skill",
        version="1.0.0"
    )
    with pytest.raises(UnauthorizedSkillInvocationError):
        tool_skill_invocation(inp)
