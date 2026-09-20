from pydantic import BaseModel, Field

class F15Input(BaseModel):
    tool: str = Field(..., description="Canonical tool name e.g. file.read, shell.write")
    path: str = Field(..., description="Target file path or command scope")
    policy_revision: int = Field(..., ge=0, description="Active policy revision")

class F15Output(BaseModel):
    decision: str = Field(..., description="allow | ask | block")
    policy_revision: int = Field(..., ge=0)

def restricted_tool_policy(input_data: F15Input) -> F15Output:
    """
    Evaluates tool proposals against restricted M0 policy rules.
    Allowed: file.read, browser.navigate, research tools.
    Ask: file.write (within workspace).
    Block: shell.outbound_write, privileged operations, unknown tools.
    """
    allowed_tools = {"file.read", "browser.navigate", "search.query"}
    ask_tools = {"file.write"}
    
    if input_data.tool in allowed_tools:
        decision = "allow"
    elif input_data.tool in ask_tools:
        decision = "ask"
    else:
        decision = "block"

    return F15Output(
        decision=decision,
        policy_revision=input_data.policy_revision,
    )
