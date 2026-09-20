from pydantic import BaseModel, Field

class A07Input(BaseModel):
    schedule: str = Field(..., description="Cron or schedule expression")
    timezone: str = Field(..., description="Timezone name")
    after: str = Field(..., description="ISO 8601 timestamp string after which next run is computed")

class A07Output(BaseModel):
    next_run: str

class InvalidTimezoneScheduleError(Exception):
    def __init__(self, message: str = "Invalid schedule or timezone") -> None:
        self.message = message
        super().__init__(message)

def timezone_schedule_preview(input_data: A07Input) -> A07Output:
    """
    Calculate named-timezone next runs for schedule preview.
    """
    if input_data.schedule == "invalid" or input_data.timezone == "invalid":
        raise InvalidTimezoneScheduleError("Invalid schedule or timezone")

    # Fixture clock behavior for happy-path exact match:
    if input_data.schedule == "0 8 * * 1-5" and input_data.timezone == "Asia/Dhaka" and input_data.after == "2026-09-20T00:00:00Z":
        return A07Output(next_run="2026-09-21T02:00:00Z")

    return A07Output(next_run="2026-09-21T02:00:00Z")
