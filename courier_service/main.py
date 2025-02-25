from fastapi import FastAPI
from db.dependencies import Base, engine
from service.controllers.api import root_router
from service.core.rabbitmq.consumer import start_consumer
import threading

# Ініціалізація FastAPI
app = FastAPI()

# Створення таблиць у БД
Base.metadata.create_all(bind=engine)

# Підключення роутів
app.include_router(root_router, prefix="/api")

# Функція для запуску RabbitMQ у окремому потоці
def start_rabbitmq():
    start_consumer()

# Запуск RabbitMQ listener у окремому потоці
rabbitmq_thread = threading.Thread(target=start_rabbitmq, daemon=True)
rabbitmq_thread.start()
