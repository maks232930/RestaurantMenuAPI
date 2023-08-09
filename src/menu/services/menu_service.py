from uuid import UUID

from sqlalchemy import Result

from src.menu.models.menu_model import MenuDetailModel, MenuModel
from src.menu.repositorys.menu_repository import MenuRepository
from src.menu.schemas.menu_schema import MenuCreate, MenuUpdate
from src.menu.services.cache_service import CacheService


class MenuService:
    def __init__(self, menu_repository: MenuRepository, cache_service: CacheService):
        self.menu_repository: MenuRepository = menu_repository
        self.cache_service: CacheService = cache_service

    async def get_menu_detail(self, menu_id: UUID) -> MenuDetailModel | None:
        cache_key: str = f'menu:{menu_id}'
        result: MenuDetailModel | None = await self.cache_service.get_cache(cache_key)
        if result:
            return result

        result = await self.menu_repository.get_menu_detail(menu_id)
        await self.cache_service.set_cache(cache_key=cache_key, result=result)

        return result

    async def get_menus(self) -> list[MenuModel]:
        result: list[MenuModel] | Result = await self.cache_service.get_cache('get_menus')
        if result:
            return result

        result = await self.menu_repository.get_menus()

        await self.cache_service.set_cache(cache_key='get_menus', result=result)
        return result

    async def create_menu(self, menu_create: MenuCreate) -> MenuModel | None:
        await self.cache_service.delete_cache(['get_menus'])
        return await self.menu_repository.create_menu(menu_create)

    async def update_menu(self, menu_id: UUID, menu_update: MenuUpdate) -> MenuModel | None:
        await self.cache_service.delete_cache(
            [
                'get_menus',
                f'menu:{menu_id}'
            ]
        )
        return await self.menu_repository.update_menu(menu_id, menu_update)

    async def delete_menu(self, menu_id: UUID) -> MenuModel | None:
        await self.cache_service.delete_related_cache(repository='menu', menu_id=menu_id)

        return await self.menu_repository.delete_menu(menu_id)
