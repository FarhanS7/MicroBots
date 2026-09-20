from pydantic import BaseModel, Field

class P30Input(BaseModel):
    privacy_mode: str = Field(..., description="Privacy mode (local_only, cloud_allowed)")
    provider_id: str = Field(..., description="Selected provider identifier")

class P30Output(BaseModel):
    external_model_contact: bool
    indicator: str

class IncompatibleProviderError(Exception):
    """Raised when selecting a remote/cloud provider under local-only privacy mode."""
    def __init__(self, message: str = "Incompatible remote provider under local-only mode") -> None:
        self.message = message
        super().__init__(message)

def private_mode_indicator(input_data: P30Input) -> P30Output:
    """
    Exposes local-only mode and per-task external-service disclosure and validation.
    """
    if input_data.privacy_mode == "local_only" and "local" not in input_data.provider_id:
        raise IncompatibleProviderError("Incompatible remote provider under local-only mode")

    is_external = input_data.privacy_mode != "local_only"
    indicator_text = "local-only" if input_data.privacy_mode == "local_only" else "cloud-enabled"

    return P30Output(
        external_model_contact=is_external,
        indicator=indicator_text,
    )
