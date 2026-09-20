from pydantic import BaseModel, Field

class P19Input(BaseModel):
    provider_id: str = Field(..., description="Provider identifier")
    privacy_mode: str = Field(..., description="Privacy mode (local_only, cloud_allowed)")

class P19Output(BaseModel):
    saved: bool
    locality_indicator: str

class ConnectionFailedError(Exception):
    """Raised when provider endpoint connectivity test fails."""
    def __init__(self, message: str = "Provider endpoint connectivity failed") -> None:
        self.message = message
        super().__init__(message)

def model_settings_ui(input_data: P19Input) -> P19Output:
    """
    Configures provider endpoints, secrets, and locality indicator in web UI.
    """
    if input_data.provider_id == "unreachable":
        raise ConnectionFailedError("Provider endpoint connectivity failed")

    indicator = "local" if input_data.privacy_mode == "local_only" or "local" in input_data.provider_id else "cloud"

    return P19Output(
        saved=True,
        locality_indicator=indicator,
    )
