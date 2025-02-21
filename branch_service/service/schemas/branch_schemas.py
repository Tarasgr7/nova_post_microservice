from pydantic import BaseModel
from typing import Optional

class BranchBase(BaseModel):
    name: str
    city: str
    address: str
    phone:str
    latitude: float
    longitude: float


class BranchCreate(BranchBase):
    pass

class BranchResponse(BranchBase):
    id: int

    class Config:
        from_attributes = True

class BranchUpdate(BaseModel):
    name: Optional[str]=None
    city: Optional[str]=None
    address: Optional[str]=None
    phone:Optional[str]=None
    latitude: Optional[float]=None
    longitude: Optional[float]=None

