from src.redisclient.redisclient import RedisClient
from src.schemas.items import ItemResponse
from src.schemas.users import UserResponse 
from src.schemas.orders import OrderResponse 
import json
class Cache:
    async def get_cached_item_data(self, key: str):
        redis = await RedisClient.get_redis()
        data = await redis.get(key)
        if data is not None:
            items_data = json.loads(data)
            return [ItemResponse.model_validate(item) for item in items_data]
        return None
    async def set_cached_item_data(self, key: str, value: list[ItemResponse], expire_seconds: int = 60):
        redis = await RedisClient.get_redis()
        serialized_data = json.dumps([item.model_dump() for item in value], 
        default=str)
        await redis.setex(key,  expire_seconds, serialized_data)
        
    
    async def get_cached_profile_data(self, key: str):
        redis = await RedisClient.get_redis()
        data = await redis.get(key)
        return UserResponse.model_validate_json(data) if data is not None else None 

    async def set_cached_profile_data(self, key: str, value: UserResponse, expire_seconds: int = 60):
        redis = await RedisClient.get_redis()
        await redis.setex(key, expire_seconds, value.model_dump_json())
        return True

    async def get_cached_order_data(self, key: str):
        redis = await RedisClient.get_redis()
        data = await redis.get(key)
        if data is not None:
            orders_data = json.loads(data)
            return [OrderResponse.model_validate(order) for order in orders_data]
        return None
    async def set_cached_order_data(self, key: str, value: list[OrderResponse], expire_seconds: int = 60):
        redis = await RedisClient.get_redis()
        serialized_data = json.dumps([order.model_dump() for order in value], 
        default=str)
        await redis.setex(key,  expire_seconds, serialized_data)
