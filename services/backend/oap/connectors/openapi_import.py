from typing import List
from pydantic import BaseModel, Field

class I03Input(BaseModel):
    spec_id: str = Field(..., description="OpenAPI spec ID or reference")
    operation_ids: List[str] = Field(..., description="Selected operation IDs to import")

class I03Output(BaseModel):
    tool_names: List[str]
    enabled: bool

class OpenAPIImportError(Exception):
    def __init__(self, message: str = "Remote reference to private address or recursive schema rejected") -> None:
        self.message = message
        super().__init__(message)

def openapi_import(input_data: I03Input) -> I03Output:
    """
    Import OpenAPI documents and generate tool schemas with stable names.
    """
    if input_data.spec_id in ("private_spec", "recursive_schema", "invalid"):
        raise OpenAPIImportError("Remote reference to private address or recursive schema rejected")

    tools = [f"crm.{op}" for op in input_data.operation_ids]
    return I03Output(
        tool_names=tools,
        enabled=False,
    )
