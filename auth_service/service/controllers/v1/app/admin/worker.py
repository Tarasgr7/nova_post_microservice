from fastapi import APIRouter,status,HTTPException
from db.dependencies import logger, db_dependency
from ...utils.auth_utils import user_dependency
from db.models.worker_model import Worker
from db.models.user_model import User
from service.schemas.worker_schemas import WorkerCreate,WorkerUpdate
from ...utils.user_utils import check_admin_role
from ...utils.mongo_check import branch_exists


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_worker(worker: WorkerCreate, user: user_dependency,db:db_dependency):
    check_admin_role(user)
    existing_worker = db.query(Worker).filter(Worker.user_id == worker.user_id).first()
    if existing_worker:
        logger.warning(f"Спроба створення працівника з існуючим ID користувача: {worker.user_id}")
        raise HTTPException(status_code=400, detail="Працівник з таким ID користувача вже існує")
    user_data=db.query(User).filter(User.id == worker.user_id).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    if str(user_data.role)[9:] !="user":
        raise HTTPException(status_code=400, detail="Юзер вже працює в компанії")
    await branch_exists(worker.branch_id)
    worker_data=Worker(
      user_id=worker.user_id,
      branch_id=worker.branch_id)
    
    user_data.role = "worker"
    db.add(worker_data)
    db.commit()
    db.refresh(worker_data)
    return worker_data

@router.get("/", status_code=status.HTTP_200_OK)
def get_workers(db:db_dependency,user: user_dependency):
    check_admin_role(user)
    workers = db.query(Worker).all()
    return workers

@router.get("/{worker_id}", status_code=status.HTTP_200_OK)
def get_worker_by_id(worker_id: int, user: user_dependency,db:db_dependency):
    check_admin_role(user)
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        logger.warning(f"Працівник з ID: {worker_id} не знайдено")
        raise HTTPException(status_code=404, detail="Працівник не знайдено")
    return worker

@router.put("/{worker_id}", status_code=status.HTTP_200_OK)
async def update_worker(worker_id: int, worker_data: WorkerUpdate, user: user_dependency,db:db_dependency):
    check_admin_role(user)
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        logger.warning(f"Працівник з ID: {worker_id} не знайдено")
        raise HTTPException(status_code=404, detail="Працівник не знайдено")
    await branch_exists(worker_data.branch_id)
    worker.branch_id = worker_data.branch_id
    db.commit()
    db.refresh(worker)
    return worker

@router.delete("/{worker_id}", status_code=status.HTTP_200_OK)
def delete_worker(worker_id: int,db: db_dependency, user: user_dependency):
    check_admin_role(user)
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        logger.warning(f"Працівник з ID: {worker_id} не знайдено")
        raise HTTPException(status_code=404, detail="Працівник не знайдено")
    user_data = db.query(User).filter(User.id == worker.user_id).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    user_data.role = "user"
    db.delete(worker)
    db.commit()
    return {"message": "Працівник успішно видалено"}

