from db.models.parcel_model import Parcel
from .route_utils import check_or_create_route
def create_parcel(branch_from , branch_to,shipment_id,db):
    route = check_or_create_route(branch_from, branch_to)
    new_parcel = Parcel(route_id=route,shipment_id=shipment_id,status="awaiting_shipment")
    print("Тут є")
    db.add(new_parcel)
    db.commit()
  
