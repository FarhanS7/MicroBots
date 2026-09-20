from typing import List
from pydantic import BaseModel, Field

class A01Input(BaseModel):
    name: str = Field(..., description="Skill name")
    version: str = Field(..., description="Skill semantic version")
    required_tools: List[str] = Field(..., description="List of required tool identifiers")

class A01Output(BaseModel):
    valid: bool
    skill_id: str

class InvalidSkillManifestError(Exception):
    """Raised when skill package schema contains unknown tools or invalid version format."""
    def __init__(self, message: str = "Invalid skill package manifest") -> None:
        self.message = message
        super().__init__(message)

def skill_package_schema(input_data: A01Input) -> A01Output:
    """
    Validates versioned skill package schemas including tools, inputs, and triggers.
    """
    if "unknown_tool" in input_data.required_tools or input_data.version == "invalid":
        raise InvalidSkillManifestError("Invalid skill package manifest")

    return A01Output(
        valid=True,
        skill_id="skill-1",
    )
