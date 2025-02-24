from fastapi import APIRouter
from .route  import router as route_router



app_router = APIRouter()

app_router.include_router(route_router, prefix="/route",tags=["Try rabbit"])