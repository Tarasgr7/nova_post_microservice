from fastapi import APIRouter,HTTPException,status
from decimal import Decimal
from db.dependencies import logger,db_dependency
from db.models.shipment_model import Shipment,ShipmentStatus
from service.schemas.shipment_schema import ShipmentUpdate,ShipmentCreate
from ..utils.auth import user_dependency
from ..utils.barcode import generate_barcode
from ..utils.mongo_check import check_user_in_mongo,branch_exists
from ..utils.shipment_utils import create_tracking_number,add_shipment_status,existing_status,calculate_distance,calculate_delivery_price
from service.core.rabbitmq.producer import delete_shipment_in_service


router=APIRouter()


@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_shipment(shipment:ShipmentCreate, user:user_dependency, db:db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    await check_user_in_mongo(shipment.receiver_id)
    if user.get('id')== shipment.receiver_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ви не можете відправляти власні посилки собі")
    if shipment.branch_from == shipment.branch_to:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Bad branch id")
    branch_from_geo = await branch_exists(shipment.branch_from)
    branch_to_geo = await branch_exists(shipment.branch_to)
    distance=calculate_distance(Decimal(branch_from_geo.get('latitude')),Decimal(branch_from_geo.get('longitude')),Decimal(branch_to_geo.get('latitude')),Decimal(branch_to_geo.get('longitude')))
    price = calculate_delivery_price(distance, shipment.weight, shipment.length, shipment.width)
    tracking_number=create_tracking_number(db)
    barcode_path=f"static/barcodes/{tracking_number}.png"
    create_shipment=Shipment(
        tracking_number=tracking_number,
        sender_id=user.get('id'),
        receiver_id=shipment.receiver_id,
        branch_from=shipment.branch_from,
        branch_to=shipment.branch_to,
        weight=shipment.weight,
        length=shipment.length,
        width=shipment.width,
        status='created',
        price=price,
        barcode_path=barcode_path)
    db.add(create_shipment)
    db.commit()
    generate_barcode(tracking_number, tracking_number)
    add_shipment_status(tracking_number,'created',db)
    logger.info(f"Створення нової посилки із номером: {tracking_number}")
    db.refresh(create_shipment)
    return create_shipment

@router.get('/my-shipments', status_code=status.HTTP_200_OK)
async def get_user_shipments(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    shipments = db.query(Shipment).filter((Shipment.sender_id == user.get("id")) | (Shipment.receiver_id == user.get("id"))).all()
    return shipments

@router.get('/{tracking_number}', status_code=status.HTTP_200_OK)
async def get_shipment(tracking_number: str, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    shipment = db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Замовлення не знайдено")
    return shipment

@router.put('/change_status/{tracking_number}', status_code=status.HTTP_200_OK)
async def change_status(tracking_number: str, shipment_update: ShipmentUpdate, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    if user.get("role") not in ['admin', 'courier','worker']:
        raise HTTPException(status_code=403, detail="Тільки адміністратори, кур'єри та працівники відділення  можуть змінювати статус")
    if not existing_status(shipment_update.status):
        raise HTTPException(status_code=400, detail="Invalid status")
    shipment = db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Замовлення не знайдено")
    if user.get("role") not in ['admin', 'courier']:
        raise HTTPException(status_code=403, detail="Тільки адміністратори та кур'єри можуть змінювати статус")
    shipment.status = shipment_update.status
    db.commit()
    add_shipment_status(tracking_number, shipment_update.status, db)
    logger.info(f"Статус посилки {tracking_number} змінено на {shipment_update.status}")
    return {"message": "Статус замовлення успішно змінено"}

@router.delete('/{tracking_number}', status_code=status.HTTP_200_OK)
async def delete_shipment(tracking_number: str, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    shipment = db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Замовлення не знайдено")
    print(shipment)
    if user.get("id") != shipment.sender_id:
        raise HTTPException(status_code=403, detail="Тільки відправник може видалити замовлення")
    shipment_statuses=db.query(ShipmentStatus).filter(ShipmentStatus.shipment_id == shipment.id).all()
    for status in shipment_statuses:
        db.delete(status)
    delete_shipment_in_service(shipment)
    db.delete(shipment)
    db.commit()
    logger.info(f"Замовлення {tracking_number} видалено користувачем {user.get('id')}")
    return {"message": "Замовлення успішно видалено"}

@router.get('/{tracking_number}/statuses', status_code=status.HTTP_200_OK)
async def get_shipment_statuses(tracking_number: str, db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    shipment=db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    shipment_statuses = db.query(ShipmentStatus).filter(ShipmentStatus.shipment_id == shipment.id).all()
    return shipment_statuses