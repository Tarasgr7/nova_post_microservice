from math import radians, sin, cos, sqrt, atan2
import uuid
from db.models.shipment_model import Shipment,ShipmentStatus
from fastapi import HTTPException,status
from db.dependencies import logger,get_db
from sqlalchemy.orm import Session



def get_shipment(tracking_number: str, db):
    shipment = db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Замовлення не знайдено")
    return shipment

def create_tracking_number(db):
    status=True
    tracking_number=str(uuid.uuid4().int)[:18]
    while status:
      if  not db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first():
        status=False
        return tracking_number 

def existing_status(status):
    statuses = ["created","awaiting_shipment","in_transit","ready_for_pick_up","picked_up"]
    if status in statuses:
        return True
    else:
        return False

def add_shipment_status(tracking_number,status_shipment,db):
    print(status_shipment)
    if existing_status(status_shipment) == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")
    shipment = db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Замовлення із номером {tracking_number} не знайдено")
    shipment_status = ShipmentStatus(
        shipment_id=shipment.id,
        status=status_shipment
    )
    db.add(shipment_status)
    db.commit()



def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Радіус Землі в км
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return round(R * c,3)

def calculate_delivery_price(distance_km, weight, length, width):
    base_price = 50  # Базова вартість
    price_per_km = 0.1  # Вартість за 1 км
    weight_price = 10 * weight  # Додатковий тариф за вагу
    volume_coefficient = (length + width) / 100  # Врахування габаритів
    
    total_price = base_price + (distance_km * price_per_km) + weight_price + volume_coefficient
    return round(total_price, 2)



def change_shipment_status(shipment_id, status):
    db_generator = get_db()  # Створюємо генератор
    db: Session = next(db_generator)  # Отримуємо сесію з генератора
    try:
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        if not shipment:
            raise HTTPException(status_code=404, detail="Замовлення не знайдено")
        shipment.status = status
        add_shipment_status(shipment.tracking_number, status, db)
        db.commit()
        logger.info(f"Змінено статус замовлення {shipment.tracking_number} на {status}")
    finally:
        db_generator.close()  # Закриваємо сесію коректно





