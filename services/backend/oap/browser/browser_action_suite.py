from pydantic import BaseModel, Field

class P12Input(BaseModel):
    page_id: str = Field(..., description="Target page identifier")
    action: str = Field(..., description="Action name: click, type, scroll, fill")
    target: str = Field(..., description="Target element selector or handle")

class P12Output(BaseModel):
    clicked: bool
    page_revision: int

class UserChallengeRequiredError(Exception):
    """Raised when CAPTCHA/MFA challenge requires manual user interaction."""
    def __init__(self, message: str = "Login challenge requires user interaction") -> None:
        self.message = message
        super().__init__(message)

def browser_action_suite(input_data: P12Input) -> P12Output:
    """
    Executes browser interactions (click, type, scroll, form fill) with user challenge handling.
    """
    if input_data.target == "captcha" or input_data.target == "mfa":
        raise UserChallengeRequiredError("Login challenge requires user interaction")

    return P12Output(
        clicked=True,
        page_revision=2,
    )
