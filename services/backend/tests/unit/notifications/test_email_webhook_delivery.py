import pytest
from oap.notifications.email_webhook_delivery import (
    A12Input,
    InvalidDeliveryDestinationError,
    email_webhook_delivery,
)

def test_email_webhook_delivery_happy_path():
    inp = A12Input(
        notification_id="notification-1",
        channel="webhook",
        destination_id="destination-1"
    )
    res = email_webhook_delivery(inp)
    assert res.delivery_id == "delivery-1"
    assert res.state == "queued"

def test_email_webhook_delivery_unauthorized():
    inp = A12Input(
        notification_id="notification-1",
        channel="webhook",
        destination_id="unauthorized-destination"
    )
    with pytest.raises(InvalidDeliveryDestinationError):
        email_webhook_delivery(inp)
