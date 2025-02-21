from fastapi import APIRouter
from .app import shipment
from .app import worcker_actions

app_router = APIRouter()

app_router.include_router(shipment.router,tags=['Shipment'],prefix='/shipments')
app_router.include_router(worcker_actions.router, tags=['Worker Actions'], prefix='/worker')