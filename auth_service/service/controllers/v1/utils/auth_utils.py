import re
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime,timedelta
from typing import Annotated 
from db.models.user_model import User
from db.dependencies import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,logger
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
from jose import jwt,JWTError


from email.message import EmailMessage


oauth2_bearer=OAuth2PasswordBearer(tokenUrl='api/v1/app_auth/auth/login')


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_ukrainian_phone_number(phone_number):
    # Регулярний вираз для перевірки українського номера
    pattern = r"^(?:\+380|380|0)\d{9}$"
    
    # Видаляємо пробіли, тире та дужки для уніфікації формату
    normalized_number = re.sub(r"[ \-()]", "", phone_number)
    
    # Перевірка відповідності номеру регулярному виразу
    if not re.match(pattern, normalized_number):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Bad phone number")


def validate_password(password: str) -> bool:
    # Перевірка на мінімальну довжину 8 символів
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароль має містити не менше 8 символів."
        )
    
    # Перевірка на наявність великої літери
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароль має містити хоча б одну велику літеру."
        )
    
    # Перевірка на наявність малої літери
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароль має містити хоча б одну малу літеру."
        )
    
    # Перевірка на наявність цифри
    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароль має містити хоча б одну цифру."
        )
    
    # Перевірка на наявність спеціального символу
    if not re.search(r"[!@#$%^&*()\-_=+[\]{}|;:'\",.<>?/]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароль має містити хоча б один спеціальний символ."
        )

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def authenticate_user(email:str,password:str,db):
   user=db.query(User).filter(User.email==email).first()
   if not user or not verify_password(password, user.password_hash):
     return False
   return user




def create_access_token(email:str,id:int,role:str, expires_delta: timedelta = None):
    to_encode = {
        "sub":email,
        "id":id,
        "role":role[9:],
    }
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
   try:
      payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
      email=payload.get('sub')
      id=payload.get('id')
      role=str(payload.get('role'))
      if email is None or id is None :
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user')
      return{'email':email, 'id':id,'role':role}
   except JWTError:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Token expired')
  

user_dependency=Annotated[dict,Depends(get_current_user)]