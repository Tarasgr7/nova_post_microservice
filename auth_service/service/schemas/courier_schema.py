from pydantic import BaseModel
from typing import Optional

class CourierCreate(BaseModel):
  user_id:int
  vehicle:Optional[str] = None
  active:bool = True
  branch_from: int


class CourierUpdate(BaseModel):
  locate: Optional[str] = None
  vehicle: Optional[str] = None  # None means no change
  active: Optional[bool] = None


