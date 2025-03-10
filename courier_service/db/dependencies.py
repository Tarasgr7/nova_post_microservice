import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base,Session
from fastapi import Depends
from dotenv import load_dotenv
from typing import Annotated

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("service")

def get_db_url():
  DB_NAME=os.getenv("DB_NAME")
  DB_USER=os.getenv("DB_USER")
  DB_PASSWORD=os.getenv("DB_PASSWORD")
  DB_HOST=os.getenv("DB_HOST")
  DB_PORT=os.getenv("DB_PORT")
  return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


DATABASE_URL = get_db_url()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
  db= SessionLocal()
  try:
    yield db
  finally:
    db.close()

db_dependency=Annotated[Session,Depends(get_db)]


from .models.route_model import Route,RouteHistory
from.models.parcel_model import Parcel
from .models.courier_models import Courier



