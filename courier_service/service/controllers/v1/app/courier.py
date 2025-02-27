from fastapi import APIRouter,HTTPException,status
from db.dependencies import db_dependency, logger
from db.models.route_model import Route
from db.models.parcel_model import Parcel
from db.models.courier_models import Courier
from ..utils.auth_utils import user_dependency, check_admin_role,check_courier_role
from service.core.rabbitmq.producer import change_shipment_status_in_service

router=APIRouter()

@router.get("/routes/my", status_code=status.HTTP_200_OK)
async def get_my_route(db: db_dependency, user: user_dependency):
  if not check_courier_role(user):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ти не курьер")
  courier=db.query(Courier).filter(Courier.user_id == user.get('id')).first()
  if not courier:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Курьер не знайдений")
  routes = db.query(Route).filter(Route.courier_id == courier.id).all()
  if not routes:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Маршрути не знайдені")
  
  return routes


@router.put("/routes/{route_id}/start", status_code=status.HTTP_200_OK)
async def start_route(route_id: int, db: db_dependency, user: user_dependency):
    courier=db.query(Courier).filter(Courier.user_id == user.get('id')).first()
    if not courier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Курьер не знайдений")
    route = db.query(Route).filter(Route.courier_id == courier.id,Route.id==route_id).first()
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Маршрут не знайдений")
    print(route.status)
    if route.status != "assigned":
        raise HTTPException(status_code=400, detail="Route must be in 'assigned' status to start")
    
    route.status = "in_transit"
    parcels = db.query(Parcel).filter(Parcel.route_id == route.id).all()
    for parcel in parcels:
        parcel.status = "in_transit"
        data={
            "shipment_id":parcel.shipment_id,
            "status":"in_transit"}
        change_shipment_status_in_service(data)
    db.commit()
    return {"message": "Route started, all shipments are now in transit"}

@router.put("/routes/{route_id}/complete", status_code=status.HTTP_200_OK)
async def complete_route(route_id: int, db: db_dependency, user: user_dependency):
    courier=db.query(Courier).filter(Courier.user_id == user.get('id')).first()
    route = db.query(Route).filter(Route.courier_id == courier.id,Route.id==route_id).first()
    if route.status != "in_transit":
        raise HTTPException(status_code=400, detail="Route must be in 'in_transit' status to complete")
    route.status = "completed"
    courier.active = True
    db.commit()
    return {"message": "Route completed, shipments updated"}