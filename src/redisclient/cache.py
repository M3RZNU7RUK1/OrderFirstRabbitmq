from src.redisclient.redisclient import RedisClient
from src.schemas.items import ItemResponse
from src.schemas.users import UserResponse 

class Cache:
    async def get_cached_item_data(self, key: str):
        redis = await RedisClient.get_redis()
        data = await redis.get(key)
        return ItemResponse.model_validate_json(data) if data is not None else None 

    async def set_cached_item_data(self, key: str, value: ItemResponse, expire_seconds: int = 60):
        redis = await RedisClient.get_redis()
        await redis.setex(key,  expire_seconds, value.model_dump_json())
        return True 
    
    async def get_cached_profile_data(self, key: str):
        redis = await RedisClient.get_redis()
        data = await redis.get(key)
        return UserResponse.model_validate_json(data) if data is not None else None 

    async def set_cached_profile_data(self, key: str, value: UserResponse, expire_seconds: int = 60):
        redis = await RedisClient.get_redis()
        await redis.setex(key,  expire_seconds, value.model_dump_json())
        return True 
