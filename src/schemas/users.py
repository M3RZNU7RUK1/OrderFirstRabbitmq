from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime
    updated_at: datetime 
    orders: list["OrderResponse"]
    class Config:
        from_attributes = True 

class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str
    phone_number: str = Field(max_length=15)
    
