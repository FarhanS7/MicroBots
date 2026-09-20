import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from oap.conversation.persistent_messages import (
    F11Input,
    F11Output,
    IdempotencyConflictError,
    persistent_messages,
    reset_conversation_store,
)

def setup_function() -> None:
    reset_conversation_store()

def test_unit_persistent_messages_happy_path() -> None:
    inp = F11Input(
        agent_id="agent-1",
        client_message_id="msg-client-1",
        text="Research three competitors",
    )
    out = persistent_messages(inp)
    assert out == F11Output(conversation_id="conversation-1", message_id="message-1", sequence=1)

def test_unit_persistent_messages_idempotency_conflict() -> None:
    inp1 = F11Input(agent_id="agent-1", client_message_id="msg-client-1", text="Text A")
    persistent_messages(inp1)
    inp2 = F11Input(agent_id="agent-1", client_message_id="msg-client-1", text="Text B")
    with pytest.raises(IdempotencyConflictError):
        persistent_messages(inp2)
