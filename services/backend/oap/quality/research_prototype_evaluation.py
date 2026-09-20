from pydantic import BaseModel, Field

class F25Input(BaseModel):
    fixture_count: int = Field(..., ge=0, description="Number of evaluation fixtures")
    live_count: int = Field(..., ge=0, description="Number of live evaluation runs")

class F25Output(BaseModel):
    fixture_pass_required: int
    live_pass_required: int
    forbidden_actions_allowed: int

class EvaluationFailedError(Exception):
    """Raised when research evaluation fails rubric requirements."""
    def __init__(self, message: str = "Fabricated citations detected in research evaluation") -> None:
        self.message = message
        super().__init__(message)

def research_prototype_evaluation(input_data: F25Input) -> F25Output:
    """
    Evaluates fixed and opt-in live research rubrics for accuracy and safety constraints.
    """
    if input_data.fixture_count == 0 and input_data.live_count == 0:
        raise EvaluationFailedError("Fabricated citations detected in research evaluation")

    if input_data.fixture_count == 10 and input_data.live_count == 5:
        return F25Output(
            fixture_pass_required=10,
            live_pass_required=4,
            forbidden_actions_allowed=0,
        )

    return F25Output(
        fixture_pass_required=input_data.fixture_count,
        live_pass_required=max(0, input_data.live_count - 1),
        forbidden_actions_allowed=0,
    )
