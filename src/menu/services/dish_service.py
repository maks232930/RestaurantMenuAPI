from uuid import UUID

from sqlalchemy import Result

from src.menu.models.dish_model import DishModel
from src.menu.repositorys.dish_repository import DishRepository
from src.menu.schemas.dish_schema import DishCreate, DishUpdate
from src.menu.services.cache_service import CacheService


class DishService:
    def __init__(self, dish_repository: DishRepository, cache_service: CacheService):
        self.dish_repository: DishRepository = dish_repository
        self.cache_service: CacheService = cache_service

    async def get_dish(self, dish_id: UUID, submenu_id: UUID, menu_id: UUID) -> DishModel | None:
        cache_key: str = f'menu:{menu_id}:submenu:{submenu_id}:dish:{dish_id}'
        result: DishModel | None = await self.cache_service.get_cache(cache_key)
        if result:
            return result

        result = await self.dish_repository.get_dish(dish_id)

        await self.cache_service.set_cache(cache_key=cache_key, result=result)
        return result

    async def get_dishes(self, submenu_id: UUID, menu_id: UUID) -> list[DishModel]:
        cache_key: str = f'get_dishes:{menu_id}:{submenu_id}'
        result: list[DishModel] | Result | None = await self.cache_service.get_cache(cache_key)
        if result:
            return result

        result = await self.dish_repository.get_dishes(submenu_id)
        await self.cache_service.set_cache(cache_key=cache_key, result=result)
        return result

    async def create_dish(self, submenu_id: UUID, dish_create: DishCreate, menu_id: UUID) -> DishModel | None:
        await self.cache_service.delete_cache(
            [
                f'menu:{menu_id}',
                f'menu:{menu_id}:submenu:{submenu_id}',
                f'get_dishes:{menu_id}:{submenu_id}'
            ]
        )
        return await self.dish_repository.create_dish(submenu_id, dish_create)

    async def update_dish(self, dish_id: UUID, dish_update: DishUpdate, menu_id: UUID, submenu_id: UUID) \
            -> DishModel | None:

        await self.cache_service.delete_cache(
            [
                f'get_dishes:{menu_id}:{submenu_id}',
                f'menu:{menu_id}:submenu:{submenu_id}:dish:{dish_id}'
            ]
        )
        return await self.dish_repository.update_dish(dish_id, dish_update)

    async def delete_menu(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> DishModel | None:
        result = await self.dish_repository.delete_dish(dish_id)
        await self.cache_service.delete_related_cache(repository='dish', menu_id=menu_id, submenu_id=submenu_id,
                                                      dish_id=dish_id)

        return result
