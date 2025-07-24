from src.schemas.users import UserResponse
from src.schemas.orders import OrderResponse

UserResponse.model_rebuild()
OrderResponse.model_rebuild()
