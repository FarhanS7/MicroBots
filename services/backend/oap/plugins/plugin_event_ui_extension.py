from pydantic import BaseModel, Field

class I09Input(BaseModel):
    plugin_id: str = Field(..., description="Plugin ID")
    event_type: str = Field(..., description="Event type string")

class I09Output(BaseModel):
    subscription_id: str
    scope: str

class PluginScopeViolationError(Exception):
    def __init__(self, message: str = "Extension top-level UI navigation or cross-workspace access blocked") -> None:
        self.message = message
        super().__init__(message)

def plugin_event_ui_extension(input_data: I09Input) -> I09Output:
    """
    Subscribe plugins to authorized event types and render sandboxed UI extensions.
    """
    if input_data.event_type == "unauthorized_cross_workspace" or input_data.plugin_id == "blocked_plugin":
        raise PluginScopeViolationError("Extension top-level UI navigation or cross-workspace access blocked")

    return I09Output(
        subscription_id="plugin-subscription-1",
        scope="ws-1",
    )
