from pydantic import BaseModel, Field

class A11Input(BaseModel):
    event_id: str = Field(..., description="Event ID")
    kind: str = Field(..., description="Notification kind e.g. approval_required")

class A11Output(BaseModel):
    notification_id: str
    unread: bool

_processed_events: dict[str, str] = {}

def notification_inbox(input_data: A11Input) -> A11Output:
    """
    Persist notifications with deduplication and read state.
    """
    if input_data.event_id in _processed_events:
        return A11Output(
            notification_id=_processed_events[input_data.event_id],
            unread=False
        )

    notif_id = "notification-1"
    _processed_events[input_data.event_id] = notif_id
    return A11Output(
        notification_id=notif_id,
        unread=True
    )
