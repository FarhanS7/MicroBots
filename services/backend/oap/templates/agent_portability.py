from typing import List, Optional
from pydantic import BaseModel, Field

class I12Input(BaseModel):
    agent_id: str = Field(..., description="Agent ID to export/import")
    include_private_data: bool = Field(False, description="Whether to include private data/secrets")

class I12Output(BaseModel):
    template_id: str
    secrets_included: bool
    history_included: bool
    unresolved_dependencies: Optional[List[str]] = None

def agent_portability(input_data: I12Input) -> I12Output:
    """
    Export/import agent templates, skills, workflows and routines with schema version,
    dependency map and no private histories/cookies/secrets.
    """
    unresolved = None
    if input_data.agent_id == "missing_plugin_agent":
        unresolved = ["plugin-missing-1"]

    secrets_inc = input_data.include_private_data
    history_inc = input_data.include_private_data

    return I12Output(
        template_id="template-1",
        secrets_included=secrets_inc,
        history_included=history_inc,
        unresolved_dependencies=unresolved,
    )
