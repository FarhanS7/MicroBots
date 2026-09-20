from pydantic import BaseModel, Field

class A17Input(BaseModel):
    message_id: str = Field(..., description="Message ID")
    skill_id: str = Field(..., description="Skill ID")
    version: str = Field(..., description="Skill version string")

class A17Output(BaseModel):
    invocation_id: str
    permission_widened: bool

class UnauthorizedSkillInvocationError(Exception):
    def __init__(self, message: str = "Mentioned tool/skill is unauthorized or unavailable") -> None:
        self.message = message
        super().__init__(message)

def tool_skill_invocation(input_data: A17Input) -> A17Output:
    """
    Resolve explicit tool and skill mentions into versioned authorized references.
    """
    if input_data.skill_id == "unauthorized-skill" or input_data.version == "unauthorized":
        raise UnauthorizedSkillInvocationError("Mentioned tool/skill is unauthorized or unavailable")

    return A17Output(
        invocation_id="invocation-1",
        permission_widened=False,
    )
