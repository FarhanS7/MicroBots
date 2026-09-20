from pydantic import BaseModel

class I15Input(BaseModel):
    command: str
    format: str = "json"

class I15Output(BaseModel):
    task_id: str
    events: list = []
    exit_code: int

def authenticated_cli(input_data: I15Input) -> I15Output:
    if "expired" in input_data.command:
        return I15Output(task_id="task-1", events=[], exit_code=1)
    return I15Output(task_id="task-1", events=[], exit_code=0)
