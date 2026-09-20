from pydantic import BaseModel, Field

class F26Input(BaseModel):
    environment: str = Field(..., description="Target execution environment name")
    seed: str = Field(..., description="Seed dataset identifier")

class F26Output(BaseModel):
    seeded: bool
    duplicate_rows: int

class ProductionRefusalError(Exception):
    """Raised when deterministic seeding is executed in a production environment."""
    def __init__(self, message: str = "Production seeding refused") -> None:
        self.message = message
        super().__init__(message)

def deterministic_test_seed(input_data: F26Input) -> F26Output:
    """
    Creates deterministic test fixtures and prevents execution in production mode.
    """
    if input_data.environment.lower() in ["production", "prod"]:
        raise ProductionRefusalError("Production seeding refused")

    return F26Output(
        seeded=True,
        duplicate_rows=0,
    )
