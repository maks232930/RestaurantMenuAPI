from typing import Optional, List
from uuid import UUID

from src.menu.models.dish_model import DishModel
from src.menu.repositorys.dish_repository import DishRepository
from src.menu.schemas.dish_schema import DishCreate, DishUpdate


class DishService:
    def __init__(self, dish_repository: DishRepository):
        self.dish_repository = dish_repository

    async def get_dish(self, dish_id: UUID) -> Optional[DishModel]:
        return await self.dish_repository.get_dish(dish_id)

    async def get_dishes(self, submenu_id: UUID) -> List[DishModel]:
        return await self.dish_repository.get_dishes(submenu_id)

    async def create_dish(self, submenu_id: UUID, dish_create: DishCreate) -> DishModel:
        return await self.dish_repository.create_dish(submenu_id, dish_create)

    async def update_dish(self, dish_id: UUID, dish_update: DishUpdate) -> DishModel:
        return await self.dish_repository.update_dish(dish_id, dish_update)

    async def delete_menu(self, dish_id: UUID) -> DishModel:
        return await self.dish_repository.delete_dish(dish_id)
