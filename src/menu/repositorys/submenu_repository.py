from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.menu.models.dish_model import Dish
from src.menu.models.submenu_model import SubmenuModel, SubmenuDetailModel, Submenu
from src.menu.repositorys.base_repository import BaseRepository
from src.menu.schemas.submenu_schema import SubmenuCreate, SubmenuUpdate


class SubmenuRepository(BaseRepository):
    async def get_submenu_by_id(self, submenu_id: UUID) -> SubmenuModel:
        query = select(Submenu).where(Submenu.id == submenu_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_submenu_detail(self, menu_id: UUID, submenu_id: UUID) -> Optional[SubmenuDetailModel]:
        cache_key = f'submenu:{submenu_id}'
        result: SubmenuDetailModel = await self.get_cache(cache_key)
        if result:
            return result

        submenu_query = select(
            Submenu.id,
            Submenu.title,
            Submenu.description,
            func.count(Dish.id).label("dish_count")
        ).select_from(Submenu). \
            outerjoin(Dish, Submenu.id == Dish.submenu_id). \
            where(Submenu.menu_id == menu_id, Submenu.id == submenu_id). \
            group_by(Submenu.id)

        result_submenu = await self.session.execute(submenu_query)
        submenu = result_submenu.first()

        if not submenu:
            return None

        submenu_detail = SubmenuDetailModel(
            id=submenu.id,
            title=submenu.title,
            menu_id=menu_id,
            description=submenu.description,
            dishes_count=int(submenu.dish_count) if submenu.dish_count is not None else 0
        )

        await self.set_cache(cache_key=cache_key, result=submenu_detail)

        return submenu_detail

    async def get_submenus(self, menu_id: UUID) -> List[SubmenuModel]:
        result = await self.get_cache('get_submenus')
        if result:
            return result

        query = select(Submenu).where(Submenu.menu_id == menu_id)
        result = await self.session.execute(query)
        result_all = result.scalars().all()
        await self.set_cache(cache_key='get_submenus', result=result_all)
        return result_all

    async def create_submenu(self, menu_id: UUID, submenu_create: SubmenuCreate) -> SubmenuModel:
        db_submenu = Submenu(**submenu_create.model_dump(), menu_id=menu_id)
        self.session.add(db_submenu)
        await self.session.commit()
        await self.session.refresh(db_submenu)

        await self.delete_all_cache()

        return db_submenu

    async def update_submenu(self, menu_id: UUID, submenu_id: UUID,
                             submenu_update: SubmenuUpdate) -> Optional[SubmenuModel]:
        query = update(Submenu).where(Submenu.menu_id == menu_id, Submenu.id == submenu_id).values(
            **submenu_update.model_dump())
        await self.session.execute(query)
        await self.session.commit()

        await self.delete_all_cache()

        return await self.get_submenu_by_id(submenu_id)

    async def delete_submenu(self, submenu_id: UUID) -> Optional[SubmenuModel]:
        db_submenu = await self.get_submenu_by_id(submenu_id)

        if not db_submenu:
            return None

        query = delete(Submenu).where(Submenu.id == submenu_id)
        await self.session.execute(query)
        await self.session.commit()

        await self.delete_all_cache()

        return db_submenu
