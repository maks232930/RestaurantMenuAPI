import uuid
from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.menu.api.utils import get_menu_by_id
from src.menu.models.dish_model import Dish
from src.menu.models.menu_model import Menu, MenuModel, MenuDetailModel
from src.menu.models.submenu_model import Submenu
from src.menu.schemas.menu_schema import MenuCreate, MenuUpdate

router = APIRouter(
    prefix="/api/v1",
    tags=["Menu"]
)


@router.get("/menus", response_model=List[MenuModel])
async def get_menus(session: AsyncSession = Depends(get_async_session)):
    query = select(Menu)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/menus/{menu_id}", response_model=MenuDetailModel)
async def get_menu(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    menu_query = select(Menu).where(Menu.id == menu_id)
    result_menu = await session.execute(menu_query)
    menu = result_menu.scalar()

    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")

    submenu_query = select(Submenu.id).where(Submenu.menu_id == menu_id)
    result_submenu = await session.execute(submenu_query)
    result_submenu_all = [i.id for i in result_submenu.all()]

    dish_query = select(Dish.id).where(Dish.submenu_id.in_(result_submenu_all))
    result_dish = await session.execute(dish_query)

    menu_detail = MenuDetailModel(
        id=menu.id,
        title=menu.title,
        description=menu.description,
        submenus_count=len(result_submenu_all),
        dishes_count=len(result_dish.all())
    )

    return menu_detail


@router.post("/menus", response_model=MenuModel, status_code=201)
async def create_menu(menu: MenuCreate, session: AsyncSession = Depends(get_async_session)):
    db_menu = Menu(**menu.dict())
    session.add(db_menu)
    await session.commit()
    await session.refresh(db_menu)
    return db_menu


@router.patch("/menus/{menu_id}", response_model=MenuModel)
async def update_menu(menu_id: uuid.UUID, menu: MenuUpdate, session: AsyncSession = Depends(get_async_session)):
    query = update(Menu).where(Menu.id == menu_id).values(**menu.dict())
    await session.execute(query)
    await session.commit()
    db_menu = await get_menu_by_id(menu_id, session=session)
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    return db_menu


@router.delete("/menus/{menu_id}", response_model=MenuModel)
async def delete_menu(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    db_menu = await get_menu_by_id(menu_id, session=session)
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    query = delete(Menu).where(Menu.id == menu_id)
    await session.execute(query)
    await session.commit()
    return db_menu
