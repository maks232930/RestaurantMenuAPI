from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class DishInfo(BaseModel):
    id: UUID
    title: str
    description: str
    price: Decimal


class SubmenuInfo(BaseModel):
    id: UUID
    title: str
    description: str
    dishes: list[DishInfo] = []


class MenuInfo(BaseModel):
    id: UUID
    title: str
    description: str
    submenus: list[SubmenuInfo] = []


class AllMenuModel(BaseModel):
    menu: MenuInfo
