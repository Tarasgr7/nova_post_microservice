from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from datetime import datetime
from ..dependencies import Base
class Courier(Base):
    __tablename__ = "couriers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,  nullable=False)
    vehicle = Column(String, nullable=True,default=None)
    active = Column(Boolean, default=True)
    branch_from = Column(Integer,nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)