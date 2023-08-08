from uuid import UUID

from sqlalchemy import delete, select, update

from src.menu.models.dish_model import Dish, DishModel
from src.menu.repositorys.base_repository import BaseRepository
from src.menu.schemas.dish_schema import DishCreate, DishUpdate


class DishRepository(BaseRepository):
    async def get_dish_by_id(self, dish_id: UUID) -> DishModel | None:
        query = select(Dish).where(Dish.id == dish_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_dish(self, dish_id: UUID, submenu_id: UUID, menu_id) -> DishModel | None:
        cache_key = f'menu:{menu_id}:submenu:{submenu_id}:dish:{dish_id}'
        result: DishModel = await self.get_cache(cache_key)
        if result:
            return result

        query = select(Dish).where(Dish.id == dish_id)
        db_dish = await self.session.execute(query)

        if not db_dish:
            return None

        result = db_dish.scalar()

        await self.set_cache(cache_key=cache_key, result=result)

        return result

    async def get_dishes(self, submenu_id: UUID, menu_id: UUID) -> list[DishModel]:
        cache_key = f'get_dishes:{menu_id}:{submenu_id}'
        result = await self.get_cache(cache_key)
        if result:
            return result

        query = select(Dish).where(Dish.submenu_id == submenu_id)
        result = await self.session.execute(query)
        result_all = result.scalars().all()

        await self.set_cache(cache_key=cache_key, result=result_all)
        return result_all

    async def create_dish(self, submenu_id: UUID, dish_create: DishCreate, menu_id: UUID) -> DishModel | None:
        db_dish = Dish(**dish_create.model_dump(), submenu_id=submenu_id)
        self.session.add(db_dish)
        await self.session.commit()
        await self.session.refresh(db_dish)

        await self.delete_cache(
            [
                f'menu:{menu_id}',
                f'menu:{menu_id}:submenu:{submenu_id}',
                f'get_dishes:{menu_id}:{submenu_id}'
            ]
        )

        return db_dish

    async def update_dish(self, dish_id: UUID, dish_update: DishUpdate, menu_id: UUID, submenu_id) -> DishModel | None:
        query = update(Dish).where(Dish.id == dish_id).values(**dish_update.model_dump())
        await self.session.execute(query)
        await self.session.commit()

        await self.delete_cache(
            [
                f'get_dishes:{menu_id}:{submenu_id}',
                f'menu:{menu_id}:submenu:{submenu_id}:dish:{dish_id}'
            ]
        )

        return await self.get_dish_by_id(dish_id)

    async def delete_dish(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> DishModel | None:
        db_dish = await self.get_dish_by_id(dish_id)

        if not db_dish:
            return None

        query = delete(Dish).where(Dish.id == dish_id)
        await self.session.execute(query)
        await self.session.commit()

        await self.delete_related_cache(repository='dish', menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)

        return db_dish
