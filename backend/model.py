from config import CONFIG

from datetime import datetime

from pydantic import BaseModel, Field

class MessageBase(BaseModel):
    context: str
    sign: str = "Anonymous"

class Message(MessageBase):
    create_time: datetime = Field(default_factory=lambda: datetime.now(CONFIG.tz))
