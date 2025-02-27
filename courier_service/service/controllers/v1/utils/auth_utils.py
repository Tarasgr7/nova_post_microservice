from typing import Annotated
from jose import jwt,JWTError
from db.dependencies import SECRET_KEY,ALGORITHM
from db.dependencies import logger
from fastapi import Depends, status, HTTPException
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email=payload.get('sub')
        id=payload.get('id')
        role=str(payload.get('role'))
        if email is None or id is None :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user')
        return{'email':email, 'id':id,'role':role}
    except JWTError:
        return None
    

def check_admin_role(user):
    if user.get("role") != "admin":
        logger.warning(f"Невдала спроба доступу користувача: {user.get('id')} з роллю: {user.get('role')}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ви не є адміністратором")
    logger.info(f"Користувач {user.get('id')} підтверджений як адміністратор.")
    return True

def check_courier_role(user):
    print(user.get('role'))
    if user.get("role") != "courier":
        logger.warning(f"Невдала спроба доступу користувача: {user.get('id')} з роллю: {user.get('role')}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ви не є кур'єром ")
    logger.info(f"Користувач {user.get('id')} підтверджений як кур'єр.")
    return True




user_dependency=Annotated[dict,Depends(decode_access_token)]

