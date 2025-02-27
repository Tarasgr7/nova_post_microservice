from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Boolean, TIMESTAMP, Interval
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies import Base
class Courier(Base):
    __tablename__ = "couriers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vehicle = Column(String, nullable=True,default=None)
    active = Column(Boolean, default=True)
    branch_from = Column(Integer,nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User")
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle": self.vehicle,
            "active": self.active,
            "branch_from": self.branch_from}