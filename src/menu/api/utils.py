import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.menu.models.dish import Dish
from src.menu.models.menu import Menu
from src.menu.models.submenu import Submenu


async def get_menu_by_id(menu_id: uuid.UUID, session: AsyncSession):
    query = select(Menu).where(Menu.id == menu_id)
    result = await session.execute(query)
    return result.scalar()


async def get_submenu_by_id(submenu_id: uuid.UUID, session: AsyncSession):
    query = select(Submenu).where(Submenu.id == submenu_id)
    result = await session.execute(query)
    return result.scalar()


async def get_dish_by_id(dish_id: uuid.UUID, session: AsyncSession):
    query = select(Dish).where(Dish.id == dish_id)
    result = await session.execute(query)
    return result.scalar()
