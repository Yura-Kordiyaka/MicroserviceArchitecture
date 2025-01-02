import redis.asyncio as redis
from contextlib import asynccontextmanager
from config import settings
import logging
logger = logging.getLogger(__name__)
class RedisClient:
    def __init__(self):
        self.redis_url = f"redis://:{settings.redis_settings.REDIS_USER_PASSWORD}@redis:6379"
        self.redis = None

    async def connect(self):
        self.redis = redis.from_url(self.redis_url, decode_responses=True)

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def save_data_to_redis(self, key: str, value: str, ttl: int = None):
        if not self.redis:
            await self.connect()
        if ttl:
            await self.redis.set(key, value, ex=ttl)
        else:
            await self.redis.set(key, value)

    async def get_data_from_redis(self, key: str):
        if not self.redis:
            await self.connect()
        return await self.redis.get(key)

