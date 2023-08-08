from uuid import UUID

from src.menu.models.dish_model import DishModel
from src.menu.repositorys.dish_repository import DishRepository
from src.menu.schemas.dish_schema import DishCreate, DishUpdate


class DishService:
    def __init__(self, dish_repository: DishRepository):
        self.dish_repository = dish_repository

    async def get_dish(self, dish_id: UUID, submenu_id: UUID, menu_id: UUID) -> DishModel | None:
        return await self.dish_repository.get_dish(dish_id, submenu_id, menu_id)

    async def get_dishes(self, submenu_id: UUID, menu_id: UUID) -> list[DishModel]:
        return await self.dish_repository.get_dishes(submenu_id, menu_id)

    async def create_dish(self, submenu_id: UUID, dish_create: DishCreate, menu_id: UUID) -> DishModel | None:
        return await self.dish_repository.create_dish(submenu_id, dish_create, menu_id)

    async def update_dish(self, dish_id: UUID, dish_update: DishUpdate, menu_id: UUID, submenu_id: UUID) \
            -> DishModel | None:
        return await self.dish_repository.update_dish(dish_id, dish_update, menu_id, submenu_id)

    async def delete_menu(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> DishModel | None:
        return await self.dish_repository.delete_dish(menu_id, submenu_id, dish_id)
