from fastapi import FastAPI
from db.dependencies import Base, engine
from service.controllers.api import root_router
from service.core.rabbitmq import start_worker
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(root_router,prefix="/api")

start_worker()