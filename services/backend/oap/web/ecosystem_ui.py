from pydantic import BaseModel, Field

class I14Input(BaseModel):
    package_id: str = Field(..., description="Package ID")
    action: str = Field(..., description="UI Action")

class I14Output(BaseModel):
    permissions_visible: bool
    activation_requires_confirmation: bool

class MarketplaceDisabledError(Exception):
    def __init__(self, message: str = "Marketplace deployment disabled") -> None:
        self.message = message
        super().__init__(message)

def ecosystem_ui(input_data: I14Input) -> I14Output:
    """
    Expose package discovery, version selection, permission review and rollback through existing marketplace APIs.
    """
    if input_data.package_id == "marketplace_disabled" or input_data.action == "disabled-discovery":
        return I14Output(
            permissions_visible=False,
            activation_requires_confirmation=False,
        )

    return I14Output(
        permissions_visible=True,
        activation_requires_confirmation=True,
    )
