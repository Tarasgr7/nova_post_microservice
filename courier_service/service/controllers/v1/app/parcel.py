from fastapi import APIRouter,HTTPException,status
from db.dependencies import db_dependency, logger
from db.models.parcel_model import Parcel
from ..utils.auth_utils import user_dependency, check_admin_role


router = APIRouter()


@router.get('/all',status_code=status.HTTP_200_OK)
async def get_all_parcels(db: db_dependency, user: user_dependency):
    check_admin_role(user)
    parcels = db.query(Parcel).all()
    return parcels

@router.get('/{parcel_id}', status_code=status.HTTP_200_OK)
async def get_parcel(parcel_id: int, db: db_dependency, user: user_dependency):
    check_admin_role(user)
    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Посилання не знайдено")
    return parcel

@router.get("/route/{route_id}/parcel",status_code=status.HTTP_200_OK)
async def get_parcels_by_route(route_id: int, db: db_dependency, user: user_dependency):
    check_admin_role(user)
    parcels = db.query(Parcel).filter(Parcel.route_id == route_id).all()
    return parcels
