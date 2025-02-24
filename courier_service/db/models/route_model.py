from ..dependencies import Base
from sqlalchemy import Column, UUID, ForeignKey, Float, Enum, DateTime,Integer,String
from sqlalchemy.orm import relationship
from datetime import datetime

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    name=Column(String, nullable=True)
    courier_id = Column(Integer, nullable=True, index=True)  # Кур'єр, який здійснює маршрут
    branch_from = Column(Integer, nullable=False)  # Відправний пункт
    branch_to = Column(Integer, nullable=False)  # Пункт призначення
    status = Column(Enum("assigned", "in_transit", "completed", name="route_status"), default="assigned")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    parcels = relationship("Parcel", back_populates="route")

class RouteHistory(Base):
    __tablename__ = "route_history"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    status = Column(Enum("assigned", "in_transit", "completed", name="route_status"))
    changed_at = Column(DateTime, default=datetime.utcnow)

