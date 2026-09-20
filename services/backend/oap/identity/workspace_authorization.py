from pydantic import BaseModel

class NotFoundError(Exception):
    pass

class F07Input(BaseModel):
    resource_workspace_id: str

class F07Output(BaseModel):
    authorized: bool

def workspace_authorization(inp: F07Input, actor_workspace_id: str) -> F07Output:
    if inp.resource_workspace_id != actor_workspace_id:
        raise NotFoundError("Workspace not found")
    return F07Output(authorized=True)
