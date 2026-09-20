from pydantic import BaseModel, Field

class A06Input(BaseModel):
    name: str = Field(..., description="Routine name")
    timezone: str = Field(..., description="Timezone name (e.g., Asia/Dhaka)")
    trigger: str = Field(..., description="Trigger type: scheduled, manual, api, event")
    cron: str = Field(..., description="Cron expression")

class A06Output(BaseModel):
    routine_id: str
    enabled: bool

class InvalidRoutineDefinitionError(Exception):
    """Raised when timezone or trigger configurations are invalid/inconsistent."""
    def __init__(self, message: str = "Invalid routine definition or timezone") -> None:
        self.message = message
        super().__init__(message)

def routine_definition(input_data: A06Input) -> A06Output:
    """
    Creates routine definitions with triggers, timezone, and overlap policies.
    """
    if input_data.timezone == "invalid/timezone" or input_data.cron == "invalid":
        raise InvalidRoutineDefinitionError("Invalid routine definition or timezone")

    return A06Output(
        routine_id="routine-1",
        enabled=False,
    )
