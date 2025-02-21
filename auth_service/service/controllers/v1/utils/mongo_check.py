from service.core.mongo import users_collection
from fastapi import HTTPException
async def branch_exists(branch_id):
  branch=users_collection.find_one({"_id":f"branch:{branch_id}"})
  if not branch:
    raise HTTPException(status_code=404, detail="Такий відділення не знайдено")