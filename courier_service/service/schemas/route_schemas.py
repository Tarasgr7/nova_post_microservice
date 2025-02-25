from pydantic import BaseModel
from typing import Optional

class RouteUpdate(BaseModel):
  name: Optional[str] = None
  courier_id: Optional[int] = None
  