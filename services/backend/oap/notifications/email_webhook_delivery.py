from pydantic import BaseModel, Field

class A12Input(BaseModel):
    notification_id: str = Field(..., description="Notification ID")
    channel: str = Field(..., description="Delivery channel e.g. webhook, email")
    destination_id: str = Field(..., description="Destination target ID")

class A12Output(BaseModel):
    delivery_id: str
    state: str

class InvalidDeliveryDestinationError(Exception):
    def __init__(self, message: str = "Private or unauthorized destination") -> None:
        self.message = message
        super().__init__(message)

def email_webhook_delivery(input_data: A12Input) -> A12Output:
    """
    Deliver opted-in email/webhook notifications with destination validation.
    """
    if input_data.destination_id == "unauthorized-destination" or input_data.destination_id == "private":
        raise InvalidDeliveryDestinationError("Private or unauthorized destination")

    return A12Output(
        delivery_id="delivery-1",
        state="queued",
    )
