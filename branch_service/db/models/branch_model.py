from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, TIMESTAMP, Numeric
from datetime import datetime
from ..dependencies import Base

class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    phone = Column(String)
    latitude = Column(Numeric(9, 6), nullable=False)  # Точність до 6 знаків після коми
    longitude = Column(Numeric(9, 6), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

