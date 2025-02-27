from fastapi import APIRouter, HTTPException,status
from db.dependencies import logger,db_dependency
from db.models.branch_model import Branch
from service.schemas.branch_schemas import BranchCreate,BranchUpdate
from ..utils.auth import user_dependency, check_admin_role
from service.core.mongo import collection

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_branch(branch_data: BranchCreate, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User is not authorized")
    check_admin_role(user)

    # Перевірка на існування відділення з таким ім'ям
    existing_branch = db.query(Branch).filter(Branch.name == branch_data.name).first()
    if existing_branch:
        logger.warning(f"Спроба створення відділення з існуючою назвою: {branch_data.name}")
        raise HTTPException(status_code=400, detail="Відділення з такою назвою вже існує")
    # Створення нового відділення
    new_branch = Branch(**branch_data.dict())
    db.add(new_branch)
    db.commit()
    db.refresh(new_branch)
    branch_in_mongo={
        "_id":f"branch:{new_branch.id}",
        "latitude":str(new_branch.latitude),
        "longitude":str(new_branch.longitude)}
    await collection.insert_one(branch_in_mongo)  # Зберігаємо в БД MongoDB
    logger.info(f"Нове відділення створене: {new_branch.name} з ID: {new_branch.id}")
    return new_branch

@router.get("/", status_code=status.HTTP_200_OK)
def get_branches(db: db_dependency,user:user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Авторизація обов'язкова")
    branches = db.query(Branch).all()
    logger.info(f"Отримано список всіх відділень: знайдено {len(branches)} відділень.")
    return branches

@router.get("/{branch_id}", status_code=status.HTTP_200_OK)
def get_branch(branch_id: int, db: db_dependency,user:user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User is not authorized")
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        logger.warning(f"Відділення з ID: {branch_id} не знайдено.")
        raise HTTPException(status_code=404, detail="Відділення не знайдено")
    logger.info(f"Відділення з ID: {branch_id} отримано.")
    return branch

@router.put("/{branch_id}", status_code=status.HTTP_200_OK)
def update_branch(branch_id: int, branch_data: BranchUpdate, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User is not authorized")
    check_admin_role(user)
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        logger.warning(f"Відділення з ID: {branch_id} не знайдено для оновлення.")
        raise HTTPException(status_code=404, detail="Відділення не знайдено")
    update_data=branch_data.dict(exclude_unset=True)
    # Оновлення полів відділення
    for key, value in update_data.items():
        setattr(branch, key, value)
    db.commit()
    db.refresh(branch)
    logger.info(f"Відділення з ID: {branch_id} успішно оновлено.")
    return branch

@router.delete("/{branch_id}",status_code=status.HTTP_200_OK)
async def delete_branch(branch_id: int, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User is not authorized")
    check_admin_role(user)
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        logger.warning(f"Відділення з ID: {branch_id} не знайдено для видалення.")
        raise HTTPException(status_code=404, detail="Відділення не знайдено")
    branch_id_delete = f"branch:{branch_id}"
# Видаляємо документ з MongoDB за _id
    result = await collection.delete_one({"_id": branch_id_delete})
# Перевіряємо, чи було видалено документ
    if result.deleted_count > 0:
        print(f"Відділення з ID {branch_id} успішно видалено.")
    db.delete(branch)
    db.commit()
    logger.info(f"Відділення з ID: {branch_id} успішно видалено.")
    return {"message": "Відділення успішно видалено"}