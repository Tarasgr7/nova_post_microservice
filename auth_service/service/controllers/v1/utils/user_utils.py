import uuid
from fastapi import status, HTTPException
from db.models.user_model import User
from db.dependencies import logger

def get_user_or_404(db, user_id):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"Користувач з ID {user_id} не знайдений")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def check_admin_role(user):
    if user.get("role") != "admin":
        logger.warning(f"Невдала спроба доступу користувача: {user.get('id')} з роллю: {user.get('role')}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ви не є адміністратором")
    logger.info(f"Користувач {user.get('id')} підтверджений як адміністратор.")