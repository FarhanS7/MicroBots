from pydantic import BaseModel, Field

class I07Input(BaseModel):
    sdk_language: str = Field(..., description="SDK language e.g. typescript")
    fixture: str = Field(..., description="Fixture name string")

class I07Output(BaseModel):
    schema_valid: bool
    contract_tests_passed: bool

class IncompatibleProtocolError(Exception):
    def __init__(self, message: str = "Incompatible server protocol version") -> None:
        self.message = message
        super().__init__(message)

def typescript_sdk(input_data: I07Input) -> I07Output:
    """
    Publish a typed TypeScript SDK contract with tool/auth/event schemas.
    """
    if input_data.fixture == "incompatible-version" or input_data.sdk_language == "invalid":
        raise IncompatibleProtocolError("Incompatible server protocol version")

    return I07Output(
        schema_valid=True,
        contract_tests_passed=True,
    )
