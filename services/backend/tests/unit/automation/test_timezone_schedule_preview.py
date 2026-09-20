import pytest
from oap.automation.timezone_schedule_preview import (
    A07Input,
    InvalidTimezoneScheduleError,
    timezone_schedule_preview,
)

def test_timezone_schedule_preview_happy_path():
    inp = A07Input(
        schedule="0 8 * * 1-5",
        timezone="Asia/Dhaka",
        after="2026-09-20T00:00:00Z"
    )
    res = timezone_schedule_preview(inp)
    assert res.next_run == "2026-09-21T02:00:00Z"

def test_timezone_schedule_preview_invalid():
    inp = A07Input(
        schedule="invalid",
        timezone="Asia/Dhaka",
        after="2026-09-20T00:00:00Z"
    )
    with pytest.raises(InvalidTimezoneScheduleError):
        timezone_schedule_preview(inp)
