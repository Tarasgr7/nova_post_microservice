from fastapi import APIRouter,status,HTTPException
import uuid
from service.core.rebbitmq123 import send_message,reverse_message

router = APIRouter()



@router.get("/send/{text}")
async def send_text(text: str):
    corr_id = str(uuid.uuid4())
    send_message(text)
    return {"text": text}


@router.get("/send/reverse/{text}")
async def send_reverse_text(text: str):
    corr_id = str(uuid.uuid4())
    text={"text":text}
    send_message(text)
    return {"text": text}
