from pydantic import BaseModel

class WorkerCreate(BaseModel):
  user_id: int
  branch_id: int

class WorkerUpdate(BaseModel):
  branch_id: int
