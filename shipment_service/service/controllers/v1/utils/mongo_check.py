from service.core.mongo import users_collection
from fastapi import HTTPException,status
async def check_user_in_mongo(user_id: str):
    user = await users_collection.find_one({"_id": str(user_id)})
    print(user)
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Receiver not found")

async def branch_exists(branch_id):
    branch = await users_collection.find_one({"_id":f"branch:{branch_id}"})
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Branch not found")
    return branch