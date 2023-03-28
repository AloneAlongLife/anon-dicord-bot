from model import Message, MessageBase
from swap import MESSAGE_QUEUE

from fastapi import FastAPI, status

api = FastAPI()


@api.post("/")
async def index(data: MessageBase):
    if len(data.context) > 1500 or len(data.sign) > 100:
        return "", status.HTTP_400_BAD_REQUEST
    await MESSAGE_QUEUE.put(Message.parse_obj(data))
    return None
