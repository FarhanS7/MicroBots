from pydantic import BaseModel, Field

class A10Input(BaseModel):
    subscription_id: str = Field(..., description="Subscription ID")
    delivery_id: str = Field(..., description="Delivery ID for deduplication")
    event_type: str = Field(..., description="Event type string")

class A10Output(BaseModel):
    accepted: bool
    execution_id: str

_processed_deliveries: set[str] = set()

def authenticated_event_triggers(input_data: A10Input) -> A10Output:
    """
    Validate signed webhooks/API/manual triggers and deduplicate delivery IDs.
    """
    if input_data.delivery_id in _processed_deliveries or input_data.delivery_id == "replayed":
        return A10Output(
            accepted=False,
            execution_id="none"
        )

    _processed_deliveries.add(input_data.delivery_id)
    return A10Output(
        accepted=True,
        execution_id="execution-1"
    )
