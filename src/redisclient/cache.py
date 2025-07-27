from src.redisclient.redisclient import RedisClient
from src.schemas.items import ItemResponse
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

