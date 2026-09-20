import pytest
from oap.events.authenticated_event_triggers import (
    A10Input,
    authenticated_event_triggers,
)

def test_authenticated_event_triggers_happy_path():
    inp = A10Input(
        subscription_id="subscription-1",
        delivery_id="delivery-1",
        event_type="file.created"
    )
    res = authenticated_event_triggers(inp)
    assert res.accepted is True
    assert res.execution_id == "execution-1"

def test_authenticated_event_triggers_duplicate():
    inp = A10Input(
        subscription_id="subscription-1",
        delivery_id="delivery-1",
        event_type="file.created"
    )
    res = authenticated_event_triggers(inp)
    assert res.accepted is False
    assert res.execution_id == "none"
