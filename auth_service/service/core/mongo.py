import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URL=os.getenv('MONGO_DB_URL')
client = AsyncIOMotorClient(MONGO_DB_URL)

db_mongo = client["nove_post"] # за замовчуванням використовуємо першу базу даних

# MongoDB колекція для користувачів
users_collection = db_mongo.users