from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.menu.models.dish_model import Dish, DishModel
from src.menu.schemas.dish_schema import DishCreate, DishUpdate


class DishRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_dish_by_id(self, dish_id: UUID) -> DishModel:
        query = select(Dish).where(Dish.id == dish_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_dish(self, dish_id: UUID) -> Optional[DishModel]:
        query = select(Dish).where(Dish.id == dish_id)
        db_dish = await self.session.execute(query)

        if not db_dish:
            return None

        return db_dish.scalar()

    async def get_dishes(self, submenu_id: UUID) -> List[DishModel]:
        query = select(Dish).where(Dish.submenu_id == submenu_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_dish(self, submenu_id: UUID, dish_create: DishCreate) -> DishModel:
        db_dish = Dish(**dish_create.model_dump(), submenu_id=submenu_id)
        self.session.add(db_dish)
        await self.session.commit()
        await self.session.refresh(db_dish)
        return db_dish

    async def update_dish(self, dish_id: UUID, dish_update: DishUpdate) -> DishModel:
        query = update(Dish).where(Dish.id == dish_id).values(**dish_update.model_dump())
        await self.session.execute(query)
        await self.session.commit()
        return await self.get_dish_by_id(dish_id)

    async def delete_dish(self, dish_id: UUID) -> Optional[DishModel]:
        db_dish = await self.get_dish_by_id(dish_id)

        if not db_dish:
            return None

        query = delete(Dish).where(Dish.id == dish_id)
        await self.session.execute(query)
        await self.session.commit()

        return db_dish
