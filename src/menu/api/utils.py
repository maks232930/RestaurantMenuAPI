import uuid

from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.menu.models.dish_model import Dish
from src.menu.models.menu_model import Menu
from src.menu.models.submenu_model import Submenu


async def get_menu_by_id(menu_id: uuid.UUID, session: AsyncSession) -> Menu | None:
    query: Select = select(Menu).where(Menu.id == menu_id)
    result = await session.execute(query)
    return result.scalar()


async def get_submenu_by_id(submenu_id: uuid.UUID, session: AsyncSession) -> Submenu | None:
    query: Select = select(Submenu).where(Submenu.id == submenu_id)
    result: Result = await session.execute(query)
    return result.scalar()


async def get_dish_by_id(dish_id: uuid.UUID, session: AsyncSession) -> Dish | None:
    query: Select = select(Dish).where(Dish.id == dish_id)
    result: Result = await session.execute(query)
    return result.scalar()
