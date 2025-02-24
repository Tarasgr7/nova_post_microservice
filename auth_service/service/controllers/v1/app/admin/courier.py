from fastapi import APIRouter,status,HTTPException
from db.dependencies import logger, db_dependency
from ...utils.auth_utils import user_dependency
from db.models.courier_model import Courier
from db.models.user_model import User
from service.schemas.courier_schema import CourierCreate,CourierUpdate
from ...utils.user_utils import check_admin_role
from service.core.rabbitmq.producer import create_courier_in_service
from ...utils.mongo_check import branch_exists

router = APIRouter()

@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_courier(courier_data: CourierCreate, db:db_dependency,user:user_dependency):
  check_admin_role(user)
  existing_courier = db.query(Courier).filter(Courier.user_id == courier_data.user_id).first()
  if existing_courier:
    raise HTTPException(status_code=400, detail="Courier with the same id already exists")
  user_data=db.query(User).filter(User.id == courier_data.user_id).first()
  if not user_data:
    raise HTTPException(status_code=404, detail="User not found")
  if str(user_data.role)[9:] != "user":
    raise HTTPException(status_code=400, detail="Юзер вже працює в компанії")
  await branch_exists(courier_data.branch_from)
  courier=Courier(
    user_id=courier_data.user_id,
    vehicle=courier_data.vehicle,
    active=courier_data.active,
    branch_from=courier_data.branch_from
  )
  user_data.role = "courier"
  db.add(courier)
  db.commit()
  db.refresh(courier)
  create_courier_in_service(courier)

  return courier

@router.get('/',status_code=status.HTTP_200_OK)
async def get_couriers(db: db_dependency, user: user_dependency):
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
  check_admin_role(user)
  couriers = db.query(Courier).all()
  return couriers

@router.get('/{courier_id}',status_code=status.HTTP_200_OK)
async def get_courier(courier_id: int, db: db_dependency, user: user_dependency):
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
  check_admin_role(user)
  courier = db.query(Courier).filter(Courier.id == courier_id).first()
  if not courier:
    raise HTTPException(status_code=404, detail="Courier not found")
  return courier

@router.put('/{courier_id}',status_code=status.HTTP_200_OK)
async def update_courier(courier_id: int, courier_data: CourierUpdate, db: db_dependency, user: user_dependency):
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
  check_admin_role(user)
  courier = db.query(Courier).filter(Courier.id == courier_id).first()
  if not courier:
    raise HTTPException(status_code=404, detail="Courier not found")
  if courier_data.locate:
    courier.locate = courier_data.locate
  if courier_data.active is not None:
    courier.active = courier_data.active
  courier.vehicle = courier_data.vehicle
  db.commit()
  db.refresh(courier)
  return courier

@router.delete('/{courier_id}',status_code=status.HTTP_200_OK)
async def delete_courier(courier_id: int, db: db_dependency, user: user_dependency):
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
  check_admin_role(user)
  courier = db.query(Courier).filter(Courier.id == courier_id).first()
  if not courier:
    raise HTTPException(status_code=404, detail="Courier not found")
  user_data = db.query(User).filter(User.id == courier.user_id).first()
  if not user_data:
    raise HTTPException(status_code=404, detail="User not found")
  user_data.role = "user"
  db.delete(courier)
  db.commit()