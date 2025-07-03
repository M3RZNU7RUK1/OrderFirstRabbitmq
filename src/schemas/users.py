from pydantic import BaseModel
from datetime import datetime
from src.schemas.orders import OrderResponse
from typing import List

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime