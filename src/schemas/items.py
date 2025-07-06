from pydantic import BaseModel, Field
from datetime import datetime

class ItemResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int = Field(ge=1, description="Цена должна быть ≥ 1")
    created_at: datetime
    updated_at: datetime