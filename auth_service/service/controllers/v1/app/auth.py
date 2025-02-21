from fastapi import APIRouter,status,HTTPException
from db.models.user_model import User
from db.dependencies import logger,db_dependency
from service.schemas.user_schemas import UserCreate,Token,UserLoginModel
from ..utils.barcode import *
from ..utils.auth_utils import *
from datetime import timedelta
from fastapi import APIRouter, status, HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from service.core.mongo import users_collection



import uuid


router=APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/app_auth/auth/login")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: db_dependency):
    logger.info(f"Реєстрація нового користувача: {user.email}")
    
    if db.query(User).filter_by(email=user.email).first():
        logger.warning("Email вже зареєстрований")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email already registered')
    if db.query(User).filter_by(phone=user.phone).first():
        logger.warning("Номер телефону вже зареєстрований")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Phone already registered')


    logger.info('Користувач ввів вірну позицію')
    token = str(uuid.uuid4())
    barcode_id=create_barcode_id()
    barcode_path=generate_barcode(barcode_id,barcode_id,True)
    create_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        full_name=user.full_name,
        phone=user.phone,
        role=user.role,
        barcode_id=barcode_id,
        barcode_path=barcode_path
    )
    db.add(create_user)
    db.commit()
    user_in_mongo={
        "_id":str(create_user.id),
        "email": user.email,
        "role": user.role
    }
    await users_collection.insert_one(user_in_mongo)
    logger.info(f"Користувача {user.email} зареєстровано успішно в MongoDB")
    logger.info(f"Користувача {user.email} зареєстровано успішно")
    return {"message": "Користувач був успішно зареєстрований"}

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    logger.info(f"Аутентифікація користувача: {form_data.username}")
    
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        logger.warning("Не вдалося автентифікувати користувача")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    
    token = create_access_token(
        user.email,
        user.id,
        str(user.role),
        timedelta(minutes=20)
    )
    
    logger.info(f"Користувач {user.email} успішно отримав токен")
    return {'access_token': token, 'token_type': 'bearer'}