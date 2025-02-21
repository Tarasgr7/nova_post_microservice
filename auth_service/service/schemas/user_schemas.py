from pydantic import BaseModel, EmailStr
from typing import Optional

from enum import Enum
class RoleEnum(str, Enum):
    user = "user"
    worker = "worker"
    courier = "courier"
    admin = "admin"

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str
    role: RoleEnum = RoleEnum.user  # 🔥 Додаємо роль

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    role: RoleEnum

class UserUpdateModel(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    
class UserLoginModel(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None