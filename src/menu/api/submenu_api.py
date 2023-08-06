from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.menu.models.submenu_model import SubmenuDetailModel, SubmenuModel
from src.menu.repositorys.submenu_repository import SubmenuRepository
from src.menu.schemas.submenu_schema import SubmenuCreate, SubmenuUpdate
from src.menu.services.submenu_service import SubmenuService

router = APIRouter(
    prefix='/api/v1',
    tags=['Submenu']
)


async def get_submenu_service(session: AsyncSession = Depends(get_async_session)) -> SubmenuService:
    submenu_repository = SubmenuRepository(session)
    return SubmenuService(submenu_repository)


@router.get('/menus/{menu_id}/submenus', response_model=list[SubmenuModel])
async def get_submenus(menu_id: UUID, submenu_service: SubmenuService = Depends(get_submenu_service)) -> list[
        SubmenuModel]:
    return await submenu_service.get_submenus(menu_id)


@router.get('/menus/{menu_id}/submenus/{submenu_id}', response_model=SubmenuDetailModel)
async def get_submenu(menu_id: UUID, submenu_id: UUID,
                      submenu_service: SubmenuService = Depends(get_submenu_service)) -> SubmenuDetailModel:
    submenu_detail = await submenu_service.get_submenu_detail(menu_id, submenu_id)

    if not submenu_detail:
        raise HTTPException(status_code=404, detail='submenu not found')

    return submenu_detail


@router.post('/menus/{menu_id}/submenus', response_model=SubmenuModel, status_code=201)
async def create_submenu(menu_id: UUID, submenu_create: SubmenuCreate,
                         submenu_service: SubmenuService = Depends(get_submenu_service)) -> SubmenuModel | None:
    db_submenu = await submenu_service.create_submenu(menu_id, submenu_create)
    return db_submenu


@router.patch('/menus/{menu_id}/submenus/{submenu_id}', response_model=SubmenuModel)
async def update_submenu(menu_id: UUID, submenu_id: UUID, submenu_update: SubmenuUpdate,
                         submenu_service: SubmenuService = Depends(get_submenu_service)) -> SubmenuModel | None:
    db_submenu = await submenu_service.update_submenu(menu_id, submenu_id, submenu_update)

    if not db_submenu:
        raise HTTPException(status_code=404, detail='submenu not found')

    return db_submenu


@router.delete('/menus/{menu_id}/submenus/{submenu_id}', response_model=SubmenuModel)
async def delete_submenu(submenu_id: UUID,
                         submenu_service: SubmenuService = Depends(get_submenu_service)) -> SubmenuModel | None:
    db_submenu = await submenu_service.delete_submenu(submenu_id)

    if not db_submenu:
        raise HTTPException(status_code=404, detail='submenu not found')

    return db_submenu
