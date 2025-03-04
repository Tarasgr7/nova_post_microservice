from fastapi import APIRouter

from .v1 import api as api_v1

root_router = APIRouter()

root_router.include_router(api_v1.app_router,prefix="/v1/courier")