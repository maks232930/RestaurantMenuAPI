import pickle
from typing import Optional, Any, List

from aioredis import from_url
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import REDIS_URL


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.REDIS_URL = REDIS_URL

    @staticmethod
    def model_encoder(obj):
        return pickle.dumps(obj)

    async def get_redis(self):
        redis = await from_url(self.REDIS_URL)
        return redis

    async def get_cache(self, cache_key: Optional[str] = None) -> Any:
        async with await self.get_redis() as redis:
            cached_result = await redis.get(cache_key)

            if cached_result:
                result_data = pickle.loads(cached_result)
            else:
                result_data = None

            return result_data

    async def set_cache(self, expiration: int = 600, cache_key: Optional[str] = None, result: Any = None) -> None:
        async with await self.get_redis() as redis:
            serialized_result = self.model_encoder(result)
            await redis.setex(cache_key, expiration, serialized_result)

    async def delete_cache(self, cache_keys: List[str]) -> None:
        async with await self.get_redis() as redis:
            for key in cache_keys:
                redis.delete(key)

    async def delete_all_cache(self) -> None:
        async with await self.get_redis() as redis:
            await redis.flushdb(asynchronous=True)
