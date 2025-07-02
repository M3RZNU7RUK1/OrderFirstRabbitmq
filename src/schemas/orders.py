from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OrderResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    title: Optional[str] = None
    data: Optional[str] = None

    class Config:
        from_attributes = True