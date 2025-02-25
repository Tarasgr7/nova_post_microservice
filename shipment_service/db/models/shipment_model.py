from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP,Enum,ForeignKey

from datetime import datetime
from sqlalchemy.orm import relationship
from db.dependencies import Base
import enum

class ShipmentStatuses(enum.Enum):
    created="created"
    awaiting_shipment="awaiting_shipment"
    in_transit="in_transit"
    ready_for_pick_up="ready_for_pick_up"
    picked_up="picked_up"

class PaymentStatuses(enum.Enum):
    paid="paid"
    unpaid="unpaid"

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, unique=True, nullable=False)
    sender_id = Column(Integer, nullable=True)
    receiver_id = Column(Integer, nullable=True)
    branch_from = Column(Integer, nullable=True)
    branch_to = Column(Integer, nullable=True)
    location=Column(Integer, nullable=True)
    weight = Column(DECIMAL(10,2), nullable=False)
    length = Column(DECIMAL(10, 2), nullable=False)
    width = Column(DECIMAL(10, 2), nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)
    payment_status = Column(Enum(PaymentStatuses), nullable=False, default=PaymentStatuses.unpaid)  
    status = Column(Enum(ShipmentStatuses), nullable=False, default=ShipmentStatuses.created)
    barcode_path=Column(String, nullable=True)  
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    def to_dict(self):
        return{
            "id": self.id,
            "branch_from": self.branch_from,
            "branch_to": self.branch_to,
        }


class ShipmentStatus(Base):
    __tablename__ = "shipment_statuses"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    status = Column(String, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="statuses")
Shipment.statuses = relationship("ShipmentStatus", back_populates="shipment", order_by="ShipmentStatus.updated_at")