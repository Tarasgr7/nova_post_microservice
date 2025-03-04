from fastapi import FastAPI
from db.dependencies import Base, engine
from service.controllers.api import root_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url="/api/v1/branch/docs",
    openapi_url="/api/v1/branch/openapi.json",
    redoc_url="/api/v1/branch/redoc")

app.include_router(root_router,prefix="/api")

