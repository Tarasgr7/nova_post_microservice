from fastapi import APIRouter,status,HTTPException
from db.dependencies import logger, db_dependency
from db.models.route_model import Route,RouteHistory
from ..utils.auth_utils import user_dependency, check_admin_role
from service.schemas.route_schemas import RouteUpdate
router = APIRouter()


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_route(db:db_dependency, user:user_dependency):
    check_admin_role(user)
    router = db.query(Route).all()
    return router

@router.get("/{route_id}", status_code=status.HTTP_200_OK)
async def get_route(route_id: int, db: db_dependency, user: user_dependency):
    check_admin_role(user)
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Маршрут не знайдено")
    return route

@router.put("/{route_id}",status_code=status.HTTP_200_OK)
async def update_route(route_id: int, route_data: RouteUpdate, db: db_dependency, user: user_dependency):
    check_admin_role(user)
    route = db.query(Route).filter(Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Маршрут не знайдено")
    if route_data.name:
        route.name = route_data.name
    if route_data.courier_id:
        route.courier_id = route_data.courier_id
    db.commit()

@router.delete("/{route_id}",status_code=status.HTTP_200_OK)
async def delete_route(route_id:int,db:db_dependency,user:user_dependency):
    route=db.query(Route).filter(Route.id==route_id).first()
    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Маршрут не знайдено")
    db.delete(route)
    db.commit()
    return {"detail": "Маршрут успішно видалено"}