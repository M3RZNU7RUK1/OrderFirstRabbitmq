from pydantic import BaseModel
from datetime import datetime
from src.schemas.orders import OrderResponse

class UserResoinse(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime
    orders: list(OrderResponse)