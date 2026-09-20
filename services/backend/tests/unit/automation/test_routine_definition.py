import pytest
from oap.automation.routine_definition import (
    A06Input,
    A06Output,
    InvalidRoutineDefinitionError,
    routine_definition,
)

def test_routine_definition_happy_path():
    inp = A06Input(
        name="Morning brief",
        timezone="Asia/Dhaka",
        trigger="scheduled",
        cron="0 8 * * 1-5"
    )
    res = routine_definition(inp)
    assert res.routine_id == "routine-1"
    assert res.enabled is False

def test_routine_definition_invalid_timezone():
    inp = A06Input(
        name="Morning brief",
        timezone="invalid/timezone",
        trigger="scheduled",
        cron="0 8 * * 1-5"
    )
    with pytest.raises(InvalidRoutineDefinitionError):
        routine_definition(inp)
