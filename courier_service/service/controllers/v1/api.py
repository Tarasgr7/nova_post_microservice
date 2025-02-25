from fastapi import APIRouter
from .app import route
from .app import parcel


app_router = APIRouter()

app_router.include_router(route.router, prefix="/route",tags=["Route",])
app_router.include_router(parcel.router, prefix="/parcel", tags=["Parcel",])