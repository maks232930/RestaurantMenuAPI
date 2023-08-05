from typing import Optional, List
from uuid import UUID

from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.menu.models.dish_model import Dish
from src.menu.models.menu_model import MenuDetailModel, Menu, MenuModel
from src.menu.models.submenu_model import Submenu
from src.menu.schemas.menu_schema import MenuUpdate, MenuCreate


class MenuRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_menu_by_id(self, menu_id: UUID) -> Menu:
        query = select(Menu).where(Menu.id == menu_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_menu_detail(self, menu_id: UUID) -> Optional[MenuDetailModel]:
        subquery = select(
            Dish.submenu_id,
            func.count(Dish.id).label("submenu_dish_count")
        ).group_by(Dish.submenu_id).subquery()

        menu_query = select(
            Menu.id,
            Menu.title,
            Menu.description,
            func.count(Submenu.id).label("submenu_count"),
            func.sum(subquery.c.submenu_dish_count).label("total_dish_count")
        ).select_from(Menu).outerjoin(Submenu).outerjoin(subquery, Submenu.id == subquery.c.submenu_id).where(
            Menu.id == menu_id).group_by(Menu.id)

        result_menu = await self.session.execute(menu_query)
        menu = result_menu.first()

        if not menu:
            return None

        return MenuDetailModel(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=int(menu.submenu_count) if menu.submenu_count is not None else 0,
            dishes_count=int(menu.total_dish_count) if menu.total_dish_count is not None else 0
        )

    async def get_menus(self) -> List[MenuModel]:
        query = select(Menu)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_menu(self, menu_create: MenuCreate) -> Menu:
        db_menu = Menu(**menu_create.model_dump())
        self.session.add(db_menu)
        await self.session.commit()
        await self.session.refresh(db_menu)
        return db_menu

    async def update_menu(self, menu_id: UUID, menu_update: MenuUpdate) -> Menu:
        query = update(Menu).where(Menu.id == menu_id).values(**menu_update.model_dump())
        await self.session.execute(query)
        await self.session.commit()
        return await self.get_menu_by_id(menu_id)

    async def delete_menu(self, menu_id: UUID) -> Optional[Menu]:
        db_menu = await self.get_menu_by_id(menu_id)
        
        if not db_menu:
            return None

        query = delete(Menu).where(Menu.id == menu_id)
        await self.session.execute(query)
        await self.session.commit()

        return db_menu
