import pickle
from typing import Any

from aioredis import Redis, from_url
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import REDIS_URL


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
        self.REDIS_URL: str = REDIS_URL

    @staticmethod
    def model_encoder(obj: Any) -> bytes:
        return pickle.dumps(obj)

    async def get_redis(self) -> Redis:
        redis: Redis = await from_url(self.REDIS_URL)
        return redis

    async def get_cache(self, cache_key: str | None = None) -> Any:
        async with await self.get_redis() as redis:
            cached_result: Any = await redis.get(cache_key)

            if cached_result:
                result_data: Any = pickle.loads(cached_result)
            else:
                result_data = None

            return result_data

    async def set_cache(self, expiration: int = 3600, cache_key: str | None = None, result: Any = None) -> None:
        async with await self.get_redis() as redis:
            serialized_result: bytes = self.model_encoder(result)
            await redis.setex(cache_key, expiration, serialized_result)

    async def delete_cache(self, cache_keys: list[str]) -> None:
        async with await self.get_redis() as redis:
            await redis.unlink(*cache_keys)

    async def delete_related_cache(self, repository: str, **kwargs) -> None:
        caches_to_delete: list = []
        patterns: list = []
        cache_template: str = ''

        if repository == 'menu':
            cache_template = f'menu:{kwargs["menu_id"]}'
            cache_template_get_dishes: str = f'get_dishes:{kwargs["menu_id"]}:*'

            caches_to_delete.extend(
                [
                    'get_menus',
                    f'get_submenus:{kwargs["menu_id"]}',
                    cache_template
                ]
            )

            patterns.extend([f'{cache_template}:*', cache_template_get_dishes])
        elif repository == 'submenu':
            cache_template = f'menu:{kwargs["menu_id"]}:submenu:{kwargs["submenu_id"]}'

            caches_to_delete.extend(
                [
                    f'get_submenus:{kwargs["menu_id"]}',
                    f'menu:{kwargs["menu_id"]}',
                    f'get_dishes:{kwargs["menu_id"]}:{kwargs["submenu_id"]}',
                    cache_template
                ]
            )

            patterns.append(f'{cache_template}:*')
        elif repository == 'dish':
            caches_to_delete.extend(
                [
                    f'menu:{kwargs["menu_id"]}:submenu:{kwargs["submenu_id"]}:dish:{kwargs["dish_id"]}',
                    f'menu:{kwargs["menu_id"]}',
                    f'menu:{kwargs["menu_id"]}:submenu:{kwargs["submenu_id"]}',
                    f'get_dishes:{kwargs["menu_id"]}:{kwargs["submenu_id"]}'
                ]
            )

        caches_to_delete.append(cache_template)

        async with await self.get_redis() as redis:

            if repository == 'dish':
                return await redis.unlink(*caches_to_delete)

            for pattern in patterns:
                result: Any = await redis.scan(match=pattern)
                for key in result[1]:
                    caches_to_delete.append(key.decode('utf-8'))

            await redis.unlink(*caches_to_delete)
