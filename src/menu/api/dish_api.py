from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.menu.models.dish_model import DishModel
from src.menu.repositorys.dish_repository import DishRepository
from src.menu.schemas.dish_schema import DishCreate, DishUpdate
from src.menu.services.dish_service import DishService

router = APIRouter(
    prefix="/api/v1",
    tags=["Dish"]
)


async def get_dish_service(session: AsyncSession = Depends(get_async_session)) -> DishService:
    menu_repository = DishRepository(session)
    return DishService(menu_repository)


@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=List[DishModel])
async def get_dishes(submenu_id: UUID, dish_service: DishService = Depends(get_dish_service)):
    return await dish_service.get_dishes(submenu_id)


@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishModel)
async def get_dish(dish_id: UUID, dish_service: DishService = Depends(get_dish_service)):
    dish = await dish_service.get_dish(dish_id)

    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")

    return dish


@router.post("/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=DishModel, status_code=201)
async def create_dish(submenu_id: UUID, dish_create: DishCreate,
                      dish_service: DishService = Depends(get_dish_service)):
    db_dish = await dish_service.create_dish(submenu_id, dish_create)
    return db_dish


@router.patch("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishModel)
async def update_dish(dish_id: UUID, dish_update: DishUpdate, dish_service: DishService = Depends(get_dish_service)):
    db_dish = await dish_service.update_dish(dish_id, dish_update)

    if not db_dish:
        raise HTTPException(status_code=404, detail="dish not found")

    return db_dish


@router.delete("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=DishModel)
async def delete_dish(dish_id: UUID, dish_service: DishService = Depends(get_dish_service)):
    db_dish = await dish_service.delete_menu(dish_id)

    if not db_dish:
        raise HTTPException(status_code=404, detail="dish not found")

    return db_dish
