from fastapi import APIRouter,status,HTTPException
import uuid


router = APIRouter()



@router.get("/send/{text}")
async def send_text(text: str):
    return {'messages':text}

@router.get("/send/reverse/{text}")
async def send_reverse_text(text: str):
    return {'messages':text}

