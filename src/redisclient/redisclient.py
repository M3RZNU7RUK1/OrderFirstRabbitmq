from redis.asyncio import Redis, ConnectionPool 
from dotenv import load_dotenv 
import os 
from typing import Optional
from src.config import settings 

load_dotenv()

class RedisClient:
    _pool: Optional[ConnectionPool] = None

    @classmethod
    async def get_redis(cls):
        if cls._pool is None:
            cls._pool = ConnectionPool.from_url(
                settings.REDIS_URL,
                password=os.getenv("REDIS_PASSWORD") or None,
                db=int(os.getenv("REDIS_DB", 0)),
                decode_responses=True,
                max_connections=20
            )
        return Redis(connection_pool=cls._pool)

    @classmethod
    async def close(cls):
        if cls._pool:
            await cls._pool.disconnect()
            cls._pool = None

