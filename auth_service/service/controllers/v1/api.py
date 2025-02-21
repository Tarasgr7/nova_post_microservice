from fastapi import APIRouter

from .app import auth
from .app import users
from .app.admin import courier
from .app.admin import worker
from .app.admin import users as admin_users


app_router = APIRouter()

app_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
app_router.include_router(users.router, prefix="/users", tags=["Users"])
app_router.include_router(courier.router, prefix="/admin/courier", tags=["Admin Courier"])
app_router.include_router(worker.router, prefix="/admin/worker", tags=["Admin Worker"])
app_router.include_router(admin_users.router, prefix="/admin/users", tags=["Admin Users"])