import uuid
from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.menu.api.utils import get_submenu_by_id
from src.menu.models.dish_model import Dish
from src.menu.models.submenu_model import Submenu, SubmenuModel, SubmenuDetailModel
from src.menu.schemas.submenu_schema import SubmenuCreate, SubmenuUpdate

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
    submenu_query = select(
        Submenu.id,
        Submenu.title,
        Submenu.description,
        func.count(Dish.id).label("dish_count")
    ).select_from(Submenu). \
        outerjoin(Dish, Submenu.id == Dish.submenu_id). \
        where(Submenu.menu_id == menu_id, Submenu.id == submenu_id). \
        group_by(Submenu.id)

    result_submenu = await session.execute(submenu_query)
    submenu = result_submenu.first()

    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    submenu_detail = SubmenuDetailModel(
        id=submenu.id,
        title=submenu.title,
        menu_id=menu_id,
        description=submenu.description,
        dishes_count=int(submenu.dish_count) if submenu.dish_count is not None else 0
    )

    return submenu_detail


@router.post("/menus/{menu_id}/submenus", response_model=SubmenuModel, status_code=201)
async def create_submenu(menu_id: uuid.UUID, submenu: SubmenuCreate,
                         session: AsyncSession = Depends(get_async_session)):
    db_submenu = Submenu(**submenu.model_dump(), menu_id=menu_id)
    session.add(db_submenu)
    await session.commit()
    await session.refresh(db_submenu)
    return db_submenu


@router.patch("/menus/{menu_id}/submenus/{submenu_id}", response_model=SubmenuModel)
async def update_submenu(menu_id: uuid.UUID, submenu_id: uuid.UUID, submenu: SubmenuUpdate,
                         session: AsyncSession = Depends(get_async_session)):
    query = update(Submenu).where(Submenu.menu_id == menu_id, Submenu.id == submenu_id).values(**submenu.model_dump())
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
