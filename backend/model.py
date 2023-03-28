from config import CONFIG

from datetime import datetime

from pydantic import BaseModel, Field

class Message(BaseModel):
    create_time: datetime = Field(default_factory=lambda: datetime.now(CONFIG.tz))
    context: str
    sign: str = "Anonymous"
