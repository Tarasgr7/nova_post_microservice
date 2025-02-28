from fastapi import APIRouter, status, HTTPException
from db.dependencies import logger,db_dependency
from ..utils.auth import user_dependency
from ..utils.worker_utils import verify_worker_role
from ..utils.shipment_utils import get_shipment,add_shipment_status
from service.core.rabbitmq.producer import create_shipment_in_service


router = APIRouter()

@router.put("/accept_shipment/{tracking_number}", status_code=status.HTTP_202_ACCEPTED)
async def accept_shipment(tracking_number: str, db: db_dependency, user: user_dependency):
    verify_worker_role(user)
    shipment = get_shipment(tracking_number, db)
    
    if shipment.status == "awaiting_shipment":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Посилка вже на пошті")
    shipment.location = shipment.branch_from
    shipment.status = "awaiting_shipment"
    add_shipment_status(tracking_number, "awaiting_shipment", db)
    db.commit()
    db.refresh(shipment)
    create_shipment_in_service(shipment)
    logger.info(f"Посилка прийнята у відділення: {shipment.branch_from}")
    return {"message": "Замовлення прийнято у відділення"}

@router.put("/accept_shipment_from_courier/{tracking_number}", status_code=status.HTTP_202_ACCEPTED)
async def accept_shipment_from_courier(tracking_number: str, db: db_dependency, user: user_dependency):
    verify_worker_role(user)
    shipment = get_shipment(tracking_number, db)
    shipment.location = shipment.branch_to
    shipment.status = "ready_for_pick_up"
    add_shipment_status(tracking_number, "ready_for_pick_up", db)
    db.commit()
    logger.info(f"Посилка прибула у відділення: {shipment.branch_to}")
    return {"message": "Замовлення прийнято у відділення"}

@router.put("/pay_shipment/{tracking_number}", status_code=status.HTTP_202_ACCEPTED)
async def pay_shipment(tracking_number: str, db: db_dependency, user: user_dependency):
    verify_worker_role(user)
    shipment = get_shipment(tracking_number, db)
    if shipment.payment_status == "paid":
        raise HTTPException(status_code=400, detail="Замовлення вже оплачено")
    shipment.payment_status = "paid"
    db.commit()
    logger.info(f"Оплата посилки завершена: {tracking_number}")
    return {"message": "Оплата замовлення успішно завершена"}

@router.put("/pick_up_shipment/{tracking_number}", status_code=status.HTTP_200_OK)
async def pick_up_shipment(tracking_number: str, db: db_dependency, user: user_dependency):
    verify_worker_role(user)
    shipment = get_shipment(tracking_number, db)
    if str(shipment.status)[17:] != "ready_for_pick_up":
        raise HTTPException(status_code=400, detail="Замовлення не в стані ready_for_pick_up")
    print(str(shipment.payment_status)[16:])
    if str(shipment.payment_status)[16:] != "paid":
        raise HTTPException(status_code=400, detail="Замовлення не оплачено")
    shipment.status = "picked_up"
    add_shipment_status(tracking_number, "picked_up", db)
    db.commit()
    logger.info(f"Посилка взята у відділення: {shipment.branch_to}")
    return {"message": "Посилка взята у відділення"}
