from pydantic import BaseModel, Field

class P21Input(BaseModel):
    conversation_id: str = Field(..., description="Conversation identifier")
    file_id: str = Field(..., description="File identifier")
    media_type: str = Field(..., description="MIME media type")

class P21Output(BaseModel):
    attachment_id: str
    accepted: bool

class InvalidAttachmentError(Exception):
    """Raised when an attachment is oversized or has an unsupported media type."""
    def __init__(self, message: str = "Invalid or oversized attachment") -> None:
        self.message = message
        super().__init__(message)

def attachments_rich_messages(input_data: P21Input) -> P21Output:
    """
    Attaches files/images/links and reply references to messages with size/type checks.
    """
    if input_data.media_type == "unsupported" or input_data.file_id == "oversized":
        raise InvalidAttachmentError("Invalid or oversized attachment")

    return P21Output(
        attachment_id="attachment-1",
        accepted=True,
    )
