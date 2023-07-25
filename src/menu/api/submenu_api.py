import uuid
from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.menu.api.utils import get_submenu_by_id
from src.menu.models.dish import Dish
from src.menu.models.submenu import Submenu, SubmenuModel, SubmenuDetailModel
from src.menu.schemas import SubmenuCreate, SubmenuUpdate

router = APIRouter(
    prefix="/api/v1",
    tags=["Submenu"]
)


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
