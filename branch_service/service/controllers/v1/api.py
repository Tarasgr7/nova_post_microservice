from fastapi import APIRouter
from .app import branch

app_router = APIRouter()

app_router.include_router(branch.router, prefix="/branch", tags=["branch"])