from pydantic import BaseModel, Field
from datetime import datetime

class ItemResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True 

class NewItem(BaseModel):
    title: str
    description: str
    price: int = Field(gt=0, lt=2147483647)
