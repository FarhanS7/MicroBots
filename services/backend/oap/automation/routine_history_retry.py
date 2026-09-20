from pydantic import BaseModel, Field

class A09Input(BaseModel):
    execution_id: str = Field(..., description="Execution ID")
    failure_code: str = Field(..., description="Failure code string")
    attempt: int = Field(..., ge=0, description="Attempt number")

class A09Output(BaseModel):
    retry_scheduled: bool
    next_attempt: int

NON_RETRYABLE_CODES = {"NON_IDEMPOTENT_UNKNOWN", "UNKNOWN_EXTERNAL_RESULT", "FATAL_ERROR"}

def routine_history_retry(input_data: A09Input) -> A09Output:
    """
    Retry only retryable failures with bounded exponential backoff.
    """
    if input_data.failure_code in NON_RETRYABLE_CODES or input_data.attempt >= 3:
        return A09Output(
            retry_scheduled=False,
            next_attempt=input_data.attempt,
        )

    return A09Output(
        retry_scheduled=True,
        next_attempt=input_data.attempt + 1,
    )
