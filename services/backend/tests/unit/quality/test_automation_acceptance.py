import pytest
from oap.quality.automation_acceptance import (
    A14Input,
    automation_acceptance,
)

def test_automation_acceptance_happy_path():
    inp = A14Input(
        scenario="morning-brief",
        duplicate_trigger=True
    )
    res = automation_acceptance(inp)
    assert res.effective_runs == 1
    assert res.notification_count == 1

def test_automation_acceptance_paused():
    inp = A14Input(
        scenario="paused",
        duplicate_trigger=False
    )
    res = automation_acceptance(inp)
    assert res.effective_runs == 0
    assert res.notification_count == 0
