import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.menu.models import Menu, Submenu, Dish, MenuModel, DishModel, SubmenuModel, MenuDetailModel, SubmenuDetailModel
from src.database import get_async_session
from src.menu.schemas import MenuCreate, MenuUpdate, SubmenuCreate, SubmenuUpdate, DishCreate, DishUpdate

router = APIRouter(
    prefix="/api/v1",
    tags=["Menu"]
)


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


@router.get("/menus", response_model=List[MenuModel])
async def get_menus(session: AsyncSession = Depends(get_async_session)):
    query = select(Menu)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/menus/{menu_id}", response_model=MenuDetailModel)
async def get_menu(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    menu_query = select(Menu).where(Menu.id == menu_id)
    submenu_query = select(Submenu.id).where(Submenu.menu_id == menu_id)

    result_menu = await session.execute(menu_query)

    result_submenu = await session.execute(submenu_query)
    result_submenu_all = [i.id for i in result_submenu.all()]

    dish_query = select(Dish.id).where(Dish.submenu_id.in_(result_submenu_all))
    result_dish = await session.execute(dish_query)

    menu = result_menu.scalar()

    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")

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


@router.get("/menus/{menu_id}/submenus", response_model=List[SubmenuModel])
async def get_submenus(menu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    query = select(Submenu).where(Submenu.menu_id == menu_id)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/menus/{menu_id}/submenus/{submenu_id}", response_model=SubmenuDetailModel)
async def get_submenu(menu_id: uuid.UUID, submenu_id: uuid.UUID,
                      session: AsyncSession = Depends(get_async_session)):
    submenu_query = select(Submenu).where(Submenu.id == submenu_id)
    dish_query = select(Dish.id).where(Dish.submenu_id == submenu_id)

    result_submenu = await session.execute(submenu_query)
    result_dish = await session.execute(dish_query)

    submenu = result_submenu.scalar()
    dish = [i.id for i in result_dish.all()]

    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    submenu_detail = SubmenuDetailModel(
        id=submenu.id,
        title=submenu.title,
        menu_id=submenu.menu_id,
        description=submenu.description,
        dishes_count=len(dish)
    )

    return submenu_detail


@router.post("/menus/{menu_id}/submenus", response_model=SubmenuModel, status_code=201)
async def create_submenu(menu_id: uuid.UUID, submenu: SubmenuCreate,
                         session: AsyncSession = Depends(get_async_session)):
    db_submenu = Submenu(**submenu.dict(), menu_id=menu_id)
    session.add(db_submenu)
    await session.commit()
    await session.refresh(db_submenu)
    return db_submenu


@router.patch("/menus/{menu_id}/submenus/{submenu_id}", response_model=SubmenuModel)
async def update_submenu(menu_id: uuid.UUID, submenu_id: uuid.UUID, submenu: SubmenuUpdate,
                         session: AsyncSession = Depends(get_async_session)):
    query = update(Submenu).where(Submenu.id == submenu_id).values(**submenu.dict())
    await session.execute(query)
    await session.commit()
    db_submenu = await get_submenu_by_id(submenu_id, session=session)
    if not db_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    return db_submenu


@router.delete("/menus/{menu_id}/submenus/{submenu_id}", response_model=SubmenuModel)
async def delete_submenu(submenu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    db_submenu = await get_submenu_by_id(submenu_id, session=session)
    if not db_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    query = delete(Submenu).where(Submenu.id == submenu_id)
    await session.execute(query)
    await session.commit()
    return db_submenu


@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=List[DishModel])
async def get_dishes(submenu_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    query = select(Dish).where(Dish.submenu_id == submenu_id)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishModel)
async def get_dish(dish_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    query = select(Dish).where(Dish.id == dish_id)
    result = await session.execute(query)
    dish = result.scalar()
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish


@router.post("/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=DishModel, status_code=201)
async def create_dish(submenu_id: uuid.UUID, dish: DishCreate, session: AsyncSession = Depends(get_async_session)):
    db_dish = Dish(**dish.dict(), submenu_id=submenu_id)
    session.add(db_dish)
    await session.commit()
    await session.refresh(db_dish)
    return db_dish


@router.patch("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishModel)
async def update_dish(dish_id: uuid.UUID, dish: DishUpdate, session: AsyncSession = Depends(get_async_session)):
    query = update(Dish).where(Dish.id == dish_id).values(**dish.dict())
    await session.execute(query)
    await session.commit()
    db_dish = await get_dish_by_id(dish_id, session=session)
    if not db_dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return db_dish


@router.delete("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishModel)
async def delete_dish(dish_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    db_dish = await get_dish_by_id(dish_id, session=session)
    if not db_dish:
        raise HTTPException(status_code=404, detail="dish not found")
    query = delete(Dish).where(Dish.id == dish_id)
    await session.execute(query)
    await session.commit()
    return db_dish
