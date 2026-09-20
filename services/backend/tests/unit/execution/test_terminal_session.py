import pytest
from oap.execution.terminal_session import (
    F18Input,
    F18Output,
    DeadlineExceededError,
    terminal_session,
)

def test_unit_terminal_session_happy_path():
    inp = F18Input(
        command="printf hello",
        cwd="/workspace",
        timeout_seconds=5,
    )
    res = terminal_session(inp)
    assert isinstance(res, F18Output)
    assert res.stdout == "hello"
    assert res.stderr == ""
    assert res.exit_code == 0

def test_unit_terminal_session_deadline_exceeded():
    inp = F18Input(
        command="sleep 10",
        cwd="/workspace",
        timeout_seconds=0,
    )
    with pytest.raises(DeadlineExceededError):
        terminal_session(inp)
