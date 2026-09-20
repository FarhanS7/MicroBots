import pytest
from oap.conversation.attachments_rich_messages import (
    P21Input,
    P21Output,
    InvalidAttachmentError,
    attachments_rich_messages,
)

def test_attachments_rich_messages_happy_path():
    inp = P21Input(conversation_id="conversation-1", file_id="file-1", media_type="image/png")
    out = attachments_rich_messages(inp)
    assert out.attachment_id == "attachment-1"
    assert out.accepted is True

def test_attachments_rich_messages_invalid():
    inp = P21Input(conversation_id="conversation-1", file_id="file-1", media_type="unsupported")
    with pytest.raises(InvalidAttachmentError) as exc_info:
        attachments_rich_messages(inp)
    assert "Invalid or oversized attachment" in str(exc_info.value)
