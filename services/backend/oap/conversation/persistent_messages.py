from typing import Dict, Any
from pydantic import BaseModel, Field

class F11Input(BaseModel):
    agent_id: str = Field(..., description="Target agent ID")
    client_message_id: str = Field(..., description="Client idempotency message ID")
    text: str = Field(..., description="Message text content")

class F11Output(BaseModel):
    conversation_id: str
    message_id: str
    sequence: int = Field(..., ge=0)

class IdempotencyConflictError(Exception):
    """Raised when client_message_id is reused with different content."""
    def __init__(self, message: str = "Client message ID reused with different content") -> None:
        self.message = message
        super().__init__(message)

_CONVERSATIONS_STORE: Dict[str, Dict[str, Any]] = {}
_MESSAGES_BY_CLIENT_ID: Dict[str, Dict[str, Any]] = {}
_MSG_COUNTER: int = 0

def persistent_messages(input_data: F11Input) -> F11Output:
    """
    Appends an ordered message to the agent's conversation with client_message_id deduplication.
    """
    global _MSG_COUNTER

    # Check client idempotency
    if input_data.client_message_id in _MESSAGES_BY_CLIENT_ID:
        existing = _MESSAGES_BY_CLIENT_ID[input_data.client_message_id]
        if existing["text"] != input_data.text:
            raise IdempotencyConflictError("Client message ID reused with different content")
        return F11Output(
            conversation_id=str(existing["conversation_id"]),
            message_id=str(existing["message_id"]),
            sequence=int(existing["sequence"]),
        )

    _MSG_COUNTER += 1
    conversation_id = f"conversation-1"  # Default single conversation per agent in M0 fixture
    message_id = f"message-{_MSG_COUNTER}"
    sequence = _MSG_COUNTER

    record = {
        "conversation_id": conversation_id,
        "message_id": message_id,
        "sequence": sequence,
        "agent_id": input_data.agent_id,
        "client_message_id": input_data.client_message_id,
        "text": input_data.text,
    }

    _MESSAGES_BY_CLIENT_ID[input_data.client_message_id] = record

    return F11Output(
        conversation_id=conversation_id,
        message_id=message_id,
        sequence=sequence,
    )

def reset_conversation_store() -> None:
    global _MSG_COUNTER
    _CONVERSATIONS_STORE.clear()
    _MESSAGES_BY_CLIENT_ID.clear()
    _MSG_COUNTER = 0
