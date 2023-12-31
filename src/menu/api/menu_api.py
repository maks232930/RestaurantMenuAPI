from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.menu.api.dependencies import get_cache_service
from src.menu.models.menu_model import MenuDetailModel, MenuModel
from src.menu.models.models_for_full_menu import AllMenuModel
from src.menu.repositorys.menu_repository import MenuRepository
from src.menu.schemas.menu_schema import MenuCreate, MenuUpdate
from src.menu.services.cache_service import CacheService
from src.menu.services.menu_service import MenuService

router = APIRouter(
    prefix='/api/v1',
    tags=['Menu']
)


async def get_menu_service(
        session: AsyncSession = Depends(get_async_session),
        cache_service: CacheService = Depends(get_cache_service)) -> MenuService:
    menu_repository: MenuRepository = MenuRepository(session)
    return MenuService(menu_repository, cache_service)


@router.get('/menus', response_model=list[MenuModel])
async def get_menus(menu_service: MenuService = Depends(get_menu_service)) -> list[MenuModel] | None:
    return await menu_service.get_menus()


@router.get('/menus/full', response_model=list[AllMenuModel])
async def get_full_menu(menu_service: MenuService = Depends(get_menu_service)) -> list[AllMenuModel] | None:
    return await menu_service.get_full_menu()


@router.get('/menus/{menu_id}', response_model=MenuDetailModel)
async def get_menu(menu_id: UUID, menu_service: MenuService = Depends(get_menu_service)) -> MenuDetailModel | None:
    menu_detail: MenuDetailModel | None = await menu_service.get_menu_detail(menu_id)

    if not menu_detail:
        raise HTTPException(status_code=404, detail='menu not found')

    return menu_detail


@router.post('/menus', response_model=MenuModel, status_code=201)
async def create_menu(menu_create: MenuCreate, background_tasks: BackgroundTasks,
                      menu_service: MenuService = Depends(get_menu_service)) -> MenuModel | None:
    db_menu: MenuModel | None = await menu_service.create_menu(menu_create, background_tasks)
    return db_menu


@router.patch('/menus/{menu_id}', response_model=MenuModel)
async def update_menu(menu_id: UUID, menu_update: MenuUpdate, background_tasks: BackgroundTasks,
                      menu_service: MenuService = Depends(get_menu_service)) -> MenuModel | None:
    db_menu: MenuModel | None = await menu_service.update_menu(menu_id, menu_update, background_tasks)

    if not db_menu:
        raise HTTPException(status_code=404, detail='menu not found')

    return db_menu


@router.delete('/menus/{menu_id}', response_model=MenuModel)
async def delete_menu(menu_id: UUID, background_tasks: BackgroundTasks,
                      menu_service: MenuService = Depends(get_menu_service)) -> MenuModel | None:
    db_menu: MenuModel | None = await menu_service.delete_menu(menu_id, background_tasks)

    if not db_menu:
        raise HTTPException(status_code=404, detail='menu not found')

    return db_menu
