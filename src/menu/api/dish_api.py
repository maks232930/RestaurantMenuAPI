import uuid
from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.menu.api.utils import get_dish_by_id
from src.database import get_async_session
from src.menu.models.dish_model import DishModel, Dish
from src.menu.schemas.dish_schema import DishCreate, DishUpdate

router = APIRouter(
    prefix="/api/v1",
    tags=["Dish"]
)


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
    db_dish = Dish(**dish.model_dump(), submenu_id=submenu_id)
    session.add(db_dish)
    await session.commit()
    await session.refresh(db_dish)
    return db_dish


@router.patch("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishModel)
async def update_dish(dish_id: uuid.UUID, dish: DishUpdate, session: AsyncSession = Depends(get_async_session)):
    query = update(Dish).where(Dish.id == dish_id).values(**dish.model_dump())
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
