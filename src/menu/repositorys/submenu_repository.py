from typing import Any
from uuid import UUID

from sqlalchemy import Delete, Result, Select, Update, delete, func, select, update

from src.menu.models.dish_model import Dish
from src.menu.models.submenu_model import Submenu, SubmenuDetailModel, SubmenuModel
from src.menu.repositorys.base_repository import BaseRepository
from src.menu.schemas.submenu_schema import SubmenuCreate, SubmenuUpdate


class SubmenuRepository(BaseRepository):
    async def get_submenu_by_id(self, submenu_id: UUID) -> SubmenuModel:
        query: Select = select(Submenu).where(Submenu.id == submenu_id)
        result: Result = await self.session.execute(query)
        return result.scalar()

    async def get_submenu_detail(self, menu_id: UUID, submenu_id: UUID) -> SubmenuDetailModel | None:
        submenu_query: Select = select(
            Submenu.id,
            Submenu.title,
            Submenu.description,
            func.count(Dish.id).label('dish_count')
        ).select_from(Submenu). \
            outerjoin(Dish, Submenu.id == Dish.submenu_id). \
            where(Submenu.menu_id == menu_id, Submenu.id == submenu_id). \
            group_by(Submenu.id)

        result_submenu: Result = await self.session.execute(submenu_query)
        submenu: Any = result_submenu.first()

        if not submenu:
            return None

        submenu_detail: SubmenuDetailModel = SubmenuDetailModel(
            id=submenu.id,
            title=submenu.title,
            menu_id=menu_id,
            description=submenu.description,
            dishes_count=int(submenu.dish_count) if submenu.dish_count is not None else 0
        )

        return submenu_detail

    async def get_submenus(self, menu_id: UUID) -> list[SubmenuModel] | None:
        query: Select = select(Submenu).where(Submenu.menu_id == menu_id)
        result = await self.session.execute(query)
        result_all: list[SubmenuModel] | None = result.scalars().all()
        return result_all

    async def create_submenu(self, menu_id: UUID, submenu_create: SubmenuCreate) -> SubmenuModel:
        db_submenu: Submenu = Submenu(**submenu_create.model_dump(), menu_id=menu_id)
        self.session.add(db_submenu)
        await self.session.commit()
        await self.session.refresh(db_submenu)

        return db_submenu

    async def update_submenu(self, menu_id: UUID, submenu_id: UUID,
                             submenu_update: SubmenuUpdate) -> SubmenuModel | None:
        query: Update = update(Submenu).where(Submenu.menu_id == menu_id, Submenu.id == submenu_id).values(
            **submenu_update.model_dump())
        await self.session.execute(query)
        await self.session.commit()

        return await self.get_submenu_by_id(submenu_id)

    async def delete_submenu(self, submenu_id: UUID) -> SubmenuModel | None:
        db_submenu: SubmenuModel | None = await self.get_submenu_by_id(submenu_id)

        if not db_submenu:
            return None

        query: Delete = delete(Submenu).where(Submenu.id == submenu_id)
        await self.session.execute(query)
        await self.session.commit()

        return db_submenu
