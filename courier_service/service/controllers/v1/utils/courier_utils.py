from fastapi import HTTPException,status
from db.dependencies import get_db
from db.models.courier_models import Courier
from sqlalchemy.orm import Session



def get_not_busy_courier(branch_from):
  db: Session = next(get_db())
  courier = db.query(Courier).filter(Courier.branch_from == branch_from, Courier.active == True).first()
  if not courier:
    return None
  courier.active = False
  return courier.id