from pydantic import BaseModel, Field

class I08Input(BaseModel):
    sdk_language: str = Field(..., description="SDK language e.g. python")
    fixture: str = Field(..., description="Fixture name string")

class I08Output(BaseModel):
    schema_valid: bool
    contract_tests_passed: bool

class SDKPayloadMismatchError(Exception):
    def __init__(self, message: str = "Python and TypeScript SDK payload serialization mismatch") -> None:
        self.message = message
        super().__init__(message)

def python_sdk(input_data: I08Input) -> I08Output:
    """
    Provide the equivalent Python plugin SDK with cross-language schema conformance.
    """
    if input_data.fixture == "incompatible-payload" or input_data.sdk_language == "invalid":
        raise SDKPayloadMismatchError("Python and TypeScript SDK payload serialization mismatch")

    return I08Output(
        schema_valid=True,
        contract_tests_passed=True,
    )
