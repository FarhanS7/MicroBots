from typing import Dict
from pydantic import BaseModel, Field

class F09Input(BaseModel):
    aggregate_id: str = Field(..., description="Target domain aggregate ID")
    event_type: str = Field(..., description="Domain event type name")
    request_id: str = Field(..., description="Idempotency request identifier")

class F09Output(BaseModel):
    event_id: str
    sequence: int = Field(..., ge=0)

# Outbox store with idempotency indexing by request_id
_OUTBOX_STORE: Dict[str, Dict[str, str | int]] = {}
_SEQUENCE_COUNTER: int = 0

def transactional_outbox(input_data: F09Input) -> F09Output:
    """
    Atomically records domain event in outbox with idempotency deduplication by request_id.
    """
    global _SEQUENCE_COUNTER

    # Check for deduplication
    if input_data.request_id in _OUTBOX_STORE:
        existing = _OUTBOX_STORE[input_data.request_id]
        return F09Output(
            event_id=str(existing["event_id"]),
            sequence=int(existing["sequence"]),
        )

    _SEQUENCE_COUNTER += 1
    event_id = f"event-{_SEQUENCE_COUNTER}"
    
    _OUTBOX_STORE[input_data.request_id] = {
        "event_id": event_id,
        "aggregate_id": input_data.aggregate_id,
        "event_type": input_data.event_type,
        "sequence": _SEQUENCE_COUNTER,
    }

    return F09Output(
        event_id=event_id,
        sequence=_SEQUENCE_COUNTER,
    )

def reset_outbox() -> None:
    global _SEQUENCE_COUNTER
    _OUTBOX_STORE.clear()
    _SEQUENCE_COUNTER = 0
