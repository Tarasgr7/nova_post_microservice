from fastapi import HTTPException,status
from db.dependencies import get_db
from db.models.courier_models import Courier
from sqlalchemy.orm import Session
from db.models.route_model import Route,RouteHistory
from .courier_utils import get_not_busy_courier

def check_or_create_route(branch_from,branch_to):

  db: Session = next(get_db())
  courier_id=get_not_busy_courier(branch_from)
  check_exists_route=db.query(Route).filter(Route.branch_from==branch_from,Route.branch_to==branch_to,Route.status=="assigned").first()
  if check_exists_route:
    return check_exists_route.id
  new_route = Route(name=f"Departure from Branch ID: {branch_from} to Branch ID:{branch_to}", courier_id=courier_id, branch_from=branch_from, branch_to=branch_to)
  db.add(new_route)
  db.commit()
  db.refresh(new_route)
  print(f"Route saved with ID: {new_route.id}")
  history = RouteHistory(route_id=new_route.id, status="assigned")
  db.add(history)
  db.commit()
  return new_route.id
