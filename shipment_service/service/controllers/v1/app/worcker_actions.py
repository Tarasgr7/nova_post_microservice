from fastapi import APIRouter, status, HTTPException
from db.dependencies import logger,db_dependency
from ..utils.auth import user_dependency
from db.models.shipment_model import Shipment
from ..utils.worker_utils import verify_worker_role
from ..utils.shipment_utils import get_shipment,add_shipment_status


router = APIRouter()

@router.put("/accept_shipment/{tracking_number}", status_code=status.HTTP_202_ACCEPTED)
def accept_shipment(tracking_number: str, db: db_dependency, user: user_dependency):
    verify_worker_role(user)
    shipment = get_shipment(tracking_number, db)
    
    if shipment.status == "awaiting_shipment":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Посилка вже на пошті")
    shipment.location = shipment.branch_from
    shipment.status = "awaiting_shipment"
    add_shipment_status(tracking_number, "awaiting_shipment", db)
    db.commit()
    logger.info(f"Посилка прийнята у відділення: {shipment.branch_from}")
    return {"message": "Замовлення прийнято у відділення"}

###  Потім переробити отримання даних юзера по штрихкоду, який зберігається в мікросервісі Auth   ###

# @router.get('user_info_by_barcode/{barcode_id}',status_code=status.HTTP_200_OK)
# async def get_user_info_by_barcode(barcode_id: str, db: db_dependency,user:user_dependency):
#     verify_worker_role(user)
#     user_data = db.query(User).filter(User.barcode_id == barcode_id).first()
#     if not user_data:
#         raise HTTPException(status_code=404, detail="Користувач не знайдений")
#     shipment=db.query(Shipment).filter(Shipment.receiver_id == user_data.id).filter(Shipment.status != "picked up").all()
#     return {
#         "user_id": user_data.id,
#         "name": user_data.full_name,
#         "phone_number": user_data.phone,
#         "shipments": [
#             {"tracking_number": shipment.tracking_number, "status": shipment.status}
#             for shipment in shipment
#         ]
#     }



@router.put("/accept_shipment_from_courier/{tracking_number}", status_code=status.HTTP_202_ACCEPTED)
def accept_shipment_from_courier(tracking_number: str, db: db_dependency, user: user_dependency):
    verify_worker_role(user)
    shipment = get_shipment(tracking_number, db)
    shipment.location = shipment.branch_to
    shipment.status = "ready_for_pick_up"
    add_shipment_status(tracking_number, "ready_for_pick_up", db)
    db.commit()
    logger.info(f"Посилка прибула у відділення: {shipment.branch_to}")
    return {"message": "Замовлення прийнято у відділення"}

@router.put("/pay_shipment/{tracking_number}", status_code=status.HTTP_202_ACCEPTED)
def pay_shipment(tracking_number: str, db: db_dependency, user: user_dependency):
    verify_worker_role(user)
    shipment = get_shipment(tracking_number, db)
    if shipment.payment_status == "paid":
        raise HTTPException(status_code=400, detail="Замовлення вже оплачено")
    shipment.payment_status = "paid"
    db.commit()
    logger.info(f"Оплата посилки завершена: {tracking_number}")
    return {"message": "Оплата замовлення успішно завершена"}

@router.put("/pick_up_shipment/{tracking_number}", status_code=status.HTTP_200_OK)
def pick_up_shipment(tracking_number: str, db: db_dependency, user: user_dependency):
    verify_worker_role(user)
    shipment = get_shipment(tracking_number, db)
    if shipment.status != "ready_for_pick_up":
        raise HTTPException(status_code=400, detail="Замовлення не в стані ready_for_pick_up")
    shipment.status = "picked_up"
    db.commit()
    logger.info(f"Посилка взята у відділення: {shipment.branch_to}")
    return {"message": "Посилка взята у відділення"}
