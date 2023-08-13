from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.menu.api.dependencies import get_cache_service
from src.menu.models.dish_model import DishModel
from src.menu.repositorys.dish_repository import DishRepository
from src.menu.schemas.dish_schema import DishCreate, DishUpdate
from src.menu.services.cache_service import CacheService
from src.menu.services.dish_service import DishService

router = APIRouter(
    prefix='/api/v1',
    tags=['Dish']
)


async def get_dish_service(
        session: AsyncSession = Depends(get_async_session),
        cache_service: CacheService = Depends(get_cache_service)) -> DishService:
    dish_repository: DishRepository = DishRepository(session)
    return DishService(dish_repository, cache_service)


@router.get('/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=list[DishModel])
async def get_dishes(submenu_id: UUID, menu_id: UUID, dish_service: DishService = Depends(get_dish_service)) \
        -> list[DishModel] | None:
    return await dish_service.get_dishes(submenu_id, menu_id)


@router.get('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=DishModel)
async def get_dish(dish_id: UUID, submenu_id: UUID, menu_id: UUID,
                   dish_service: DishService = Depends(get_dish_service)) -> DishModel | None:
    dish: DishModel | None = await dish_service.get_dish(dish_id, submenu_id, menu_id)

    if not dish:
        raise HTTPException(status_code=404, detail='dish not found')

    return dish


@router.post('/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=DishModel, status_code=201)
async def create_dish(submenu_id: UUID, dish_create: DishCreate, menu_id: UUID, background_tasks: BackgroundTasks,
                      dish_service: DishService = Depends(get_dish_service)) -> DishModel | None:
    db_dish: DishModel | None = await dish_service.create_dish(submenu_id, dish_create, menu_id, background_tasks)
    return db_dish


@router.patch('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=DishModel)
async def update_dish(dish_id: UUID, dish_update: DishUpdate, menu_id: UUID, submenu_id: UUID,
                      background_tasks: BackgroundTasks,
                      dish_service: DishService = Depends(get_dish_service)) -> DishModel | None:
    db_dish: DishModel | None = await dish_service.update_dish(dish_id, dish_update, menu_id, submenu_id,
                                                               background_tasks)

    if not db_dish:
        raise HTTPException(status_code=404, detail='dish not found')

    return db_dish


@router.delete('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=DishModel)
async def delete_dish(dish_id: UUID, menu_id: UUID, submenu_id: UUID, background_tasks: BackgroundTasks,
                      dish_service: DishService = Depends(get_dish_service)) -> DishModel | None:
    db_dish: DishModel | None = await dish_service.delete_menu(menu_id, submenu_id, dish_id, background_tasks)

    if not db_dish:
        raise HTTPException(status_code=404, detail='dish not found')

    return db_dish
