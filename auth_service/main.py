from fastapi import FastAPI
from db.dependencies import Base, engine
from service.controllers.api import root_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    openapi_url="/api/v1/auth/openapi.json",
    docs_url="/api/v1/auth/docs",
    redoc_url="/api/v1/auth/redoc")

app.include_router(root_router,prefix="/api")

