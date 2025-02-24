from ..dependencies import Base
from sqlalchemy import Column, UUID, ForeignKey, Float, Enum, DateTime,Integer
from sqlalchemy.orm import relationship
from datetime import datetime

class Parcel(Base):
    __tablename__ = "parcels"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    shipment_id = Column(Integer, nullable=False)  # ID посилки із Shipment_service
    status = Column(Enum("awaiting_shipment", "in_transit", "ready_for_pick_up", "delivered", name="parcel_status"))
    added_at = Column(DateTime, default=datetime.utcnow)
    route = relationship("Route", back_populates="parcels")
