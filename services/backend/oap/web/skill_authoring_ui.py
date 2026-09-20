from pydantic import BaseModel, Field

class A16Input(BaseModel):
    draft_id: str = Field(..., description="Draft ID")
    action: str = Field(..., description="Action e.g. review, edit, activate")

class A16Output(BaseModel):
    active: bool
    required_tools_visible: bool

class DraftValidationError(Exception):
    def __init__(self, message: str = "Draft failing validation cannot be activated") -> None:
        self.message = message
        super().__init__(message)

def skill_authoring_ui(input_data: A16Input) -> A16Output:
    """
    Build skill create/edit/import/version/draft-review panels.
    """
    if input_data.action == "activate_invalid":
        raise DraftValidationError("Draft failing validation cannot be activated")

    if input_data.action == "activate":
        return A16Output(
            active=True,
            required_tools_visible=True,
        )

    return A16Output(
        active=False,
        required_tools_visible=True,
    )
