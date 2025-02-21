from pydantic import BaseModel
from typing import Optional

class CourierCreate(BaseModel):
  user_id:int
  vehicle:Optional[str] = None
  active:bool = True
  locate: str = ""  # lat, lng, address


class CourierUpdate(BaseModel):
  locate: Optional[str] = None
  vehicle: Optional[str] = None  # None means no change
  active: Optional[bool] = None


