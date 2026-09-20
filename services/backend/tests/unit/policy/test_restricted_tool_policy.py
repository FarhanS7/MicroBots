import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from oap.policy.restricted_tool_policy import (
    F15Input,
    F15Output,
    restricted_tool_policy,
)

def test_unit_restricted_tool_policy_allow() -> None:
    inp = F15Input(tool="file.read", path="notes.md", policy_revision=1)
    out = restricted_tool_policy(inp)
    assert out == F15Output(decision="allow", policy_revision=1)

def test_unit_restricted_tool_policy_block() -> None:
    inp = F15Input(tool="shell.outbound_write", path="/etc/passwd", policy_revision=1)
    out = restricted_tool_policy(inp)
    assert out == F15Output(decision="block", policy_revision=1)
