from __future__ import annotations
from pydantic import BaseModel, constr 
from datetime import datetime

class OrderResponse(BaseModel):
    id: int
    title: str
    phone_number: constr(pattern=r"^\+?[0-9\s\-]+$")
    price: int
    user: UserResponse
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

