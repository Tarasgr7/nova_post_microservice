from fastapi import APIRouter,status,HTTPException
from db.dependencies import logger, db_dependency
from ...utils.auth_utils import user_dependency
from db.models.user_model import User
from ...utils.user_utils import check_admin_role
from ...utils.user_utils import get_user_or_404

router=APIRouter()

@router.get("/read_all_users", status_code=status.HTTP_200_OK)
async def read_all_users(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    check_admin_role(user)
    users = db.query(User).all()
    logger.info(f"Отримано {len(users)} користувачів")
    return users



@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    check_admin_role(user)
    
    return get_user_or_404(db, user_id)


