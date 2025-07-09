from pydantic import BaseModel
from datetime import datetime


class OrderResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

