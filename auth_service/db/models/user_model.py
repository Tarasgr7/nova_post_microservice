from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies import Base
import enum

class UserRole(enum.Enum):
    user = "user"
    worker = "worker"
    courier = "courier"
    admin= "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    barcode_id=Column(String, nullable=True)
    barcode_path=Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    worker = relationship("Worker", back_populates="user", uselist=False)
    courier = relationship("Courier", back_populates="user", uselist=False)