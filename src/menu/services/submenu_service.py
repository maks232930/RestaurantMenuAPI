from uuid import UUID

from src.menu.models.submenu_model import SubmenuDetailModel, SubmenuModel
from src.menu.repositorys.submenu_repository import SubmenuRepository
from src.menu.schemas.submenu_schema import SubmenuCreate, SubmenuUpdate


class SubmenuService:
    def __init__(self, submenu_repository: SubmenuRepository):
        self.submenu_repository = submenu_repository

    async def get_submenu_detail(self, menu_id: UUID, submenu_id: UUID) -> SubmenuDetailModel | None:
        return await self.submenu_repository.get_submenu_detail(menu_id, submenu_id)

    async def get_submenus(self, menu_id: UUID) -> list[SubmenuModel]:
        return await self.submenu_repository.get_submenus(menu_id)

    async def create_submenu(self, menu_id: UUID, submenu_create: SubmenuCreate) -> SubmenuModel | None:
        return await self.submenu_repository.create_submenu(menu_id, submenu_create)

    async def update_submenu(self, menu_id: UUID, submenu_id: UUID, submenu_update: SubmenuUpdate) \
            -> SubmenuModel | None:
        return await self.submenu_repository.update_submenu(menu_id, submenu_id, submenu_update)

    async def delete_submenu(self, submenu_id: UUID) -> SubmenuModel | None:
        return await self.submenu_repository.delete_submenu(submenu_id)
