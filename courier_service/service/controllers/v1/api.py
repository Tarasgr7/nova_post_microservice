from fastapi import APIRouter
from .app import route
from .app import parcel
from .app import courier


app_router = APIRouter()

app_router.include_router(route.router, prefix="/route",tags=["Route",])
app_router.include_router(parcel.router, prefix="/parcel", tags=["Parcel",])
app_router.include_router(courier.router, prefix="/courier", tags=["Courier",])