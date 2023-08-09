from typing import Any
from uuid import UUID

from src.menu.models.submenu_model import SubmenuDetailModel, SubmenuModel
from src.menu.repositorys.submenu_repository import SubmenuRepository
from src.menu.schemas.submenu_schema import SubmenuCreate, SubmenuUpdate
from src.menu.services.cache_service import CacheService


class SubmenuService:
    def __init__(self, submenu_repository: SubmenuRepository, cache_service: CacheService):
        self.submenu_repository: SubmenuRepository = submenu_repository
        self.cache_service: CacheService = cache_service

    async def get_submenu_detail(self, menu_id: UUID, submenu_id: UUID) -> SubmenuDetailModel | None:
        cache_key: str = f'menu:{menu_id}:submenu:{submenu_id}'
        result: SubmenuDetailModel | None = await self.cache_service.get_cache(cache_key)
        if result:
            return result

        result = await self.submenu_repository.get_submenu_detail(menu_id, submenu_id)
        await self.cache_service.set_cache(cache_key=cache_key, result=result)

        return result

    async def get_submenus(self, menu_id: UUID) -> list[SubmenuModel] | None:
        cache_key: str = f'get_submenus:{menu_id}'
        result: list[SubmenuModel] | None | Any = await self.cache_service.get_cache(cache_key)
        if result:
            return result

        result = await self.submenu_repository.get_submenus(menu_id)
        await self.cache_service.set_cache(cache_key=cache_key, result=result)
        return result

    async def create_submenu(self, menu_id: UUID, submenu_create: SubmenuCreate) -> SubmenuModel | None:
        await self.cache_service.delete_cache(
            [
                f'menu:{menu_id}',
                f'get_submenus:{menu_id}'
            ]
        )

        return await self.submenu_repository.create_submenu(menu_id, submenu_create)

    async def update_submenu(self, menu_id: UUID, submenu_id: UUID, submenu_update: SubmenuUpdate) \
            -> SubmenuModel | None:
        await self.cache_service.delete_cache(
            [
                f'get_submenus:{menu_id}',
                f'menu:{menu_id}:submenu:{submenu_id}'
            ]
        )

        return await self.submenu_repository.update_submenu(menu_id, submenu_id, submenu_update)

    async def delete_submenu(self, submenu_id: UUID, menu_id: UUID) -> SubmenuModel | None:
        await self.cache_service.delete_related_cache(repository='submenu', menu_id=menu_id, submenu_id=submenu_id)
        return await self.submenu_repository.delete_submenu(submenu_id)
