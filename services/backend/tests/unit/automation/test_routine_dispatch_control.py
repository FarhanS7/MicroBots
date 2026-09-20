import pytest
from oap.automation.routine_dispatch_control import (
    A08Input,
    routine_dispatch_control,
)

def test_routine_dispatch_control_happy_path():
    inp = A08Input(
        routine_id="routine-1",
        scheduled_for="2026-09-21T02:00:00Z"
    )
    res = routine_dispatch_control(inp)
    assert res.execution_id == "execution-1"
    assert res.duplicate is False

def test_routine_dispatch_control_duplicate():
    inp = A08Input(
        routine_id="routine-1",
        scheduled_for="2026-09-21T02:00:00Z"
    )
    res = routine_dispatch_control(inp)
    assert res.execution_id == "execution-1"
    assert res.duplicate is True
