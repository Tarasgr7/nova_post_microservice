from pydantic import BaseModel
class ShipmentCreate(BaseModel):
    receiver_id:int
    branch_from:int
    branch_to:int
    weight: float
    length: float
    width: float

class ShipmentUpdate(BaseModel):
    status:str


class ShipmentCreateAtBranch(BaseModel):
    sender_id:int
    receiver_id:int
    branch_from:int
    branch_to:int
    weight: float
    length: float
    width: float
    payment_status : str ='unpaid'
    status: str ='awaiting shipment'

