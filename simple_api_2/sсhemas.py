from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    created_at: datetime = None
    