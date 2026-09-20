import pytest
from oap.notifications.notification_inbox import (
    A11Input,
    notification_inbox,
)

def test_notification_inbox_happy_path():
    inp = A11Input(
        event_id="event-1",
        kind="approval_required"
    )
    res = notification_inbox(inp)
    assert res.notification_id == "notification-1"
    assert res.unread is True

def test_notification_inbox_duplicate():
    inp = A11Input(
        event_id="event-1",
        kind="approval_required"
    )
    res = notification_inbox(inp)
    assert res.notification_id == "notification-1"
    assert res.unread is False
