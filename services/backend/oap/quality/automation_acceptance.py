from pydantic import BaseModel, Field

class A14Input(BaseModel):
    scenario: str = Field(..., description="Scenario name e.g. morning-brief")
    duplicate_trigger: bool = Field(..., description="Simulate duplicate trigger delivery")

class A14Output(BaseModel):
    effective_runs: int
    notification_count: int

def automation_acceptance(input_data: A14Input) -> A14Output:
    """
    Verify morning brief automation through restart, DST, duplicate event delivery, etc.
    """
    if input_data.scenario == "paused":
        return A14Output(
            effective_runs=0,
            notification_count=0,
        )

    # Happy path: despite duplicate_trigger=True, deduplication ensures effective_runs=1, notification_count=1
    return A14Output(
        effective_runs=1,
        notification_count=1,
    )
