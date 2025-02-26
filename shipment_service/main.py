from fastapi import FastAPI
from db.dependencies import Base, engine
from service.controllers.api import root_router
from service.core.rabbitmq.consumer import start_consumer
import threading


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(root_router,prefix="/api")

@app.on_event("startup")
async def startup_event():
    # Запуск асинхронного консумера
    def start_rabbitmq():
        start_consumer()
    
    # Запуск додаткових консумерів у окремому потоці
    rabbitmq_thread = threading.Thread(target=start_rabbitmq, daemon=True)
    rabbitmq_thread.start()
    print("RabbitMQ listeners запущені")