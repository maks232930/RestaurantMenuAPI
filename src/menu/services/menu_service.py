from uuid import UUID

from src.menu.models.menu_model import MenuDetailModel, MenuModel
from src.menu.repositorys.menu_repository import MenuRepository
from src.menu.schemas.menu_schema import MenuCreate, MenuUpdate


class MenuService:
    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository

    async def get_menu_detail(self, menu_id: UUID) -> MenuDetailModel | None:
        return await self.menu_repository.get_menu_detail(menu_id)

    async def get_menus(self) -> list[MenuModel]:
        return await self.menu_repository.get_menus()

    async def create_menu(self, menu_create: MenuCreate) -> MenuModel | None:
        return await self.menu_repository.create_menu(menu_create)

    async def update_menu(self, menu_id: UUID, menu_update: MenuUpdate) -> MenuModel | None:
        return await self.menu_repository.update_menu(menu_id, menu_update)

    async def delete_menu(self, menu_id: UUID) -> MenuModel | None:
        return await self.menu_repository.delete_menu(menu_id)
