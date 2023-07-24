import decimal
import uuid

from pydantic import BaseModel, UUID4
from sqlalchemy import Column, String, ForeignKey, UUID, Numeric

from src.database import Base


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(UUID, ForeignKey('menu.id', ondelete='CASCADE'), nullable=False, unique=True)


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    submenu_id = Column(UUID, ForeignKey('submenu.id', ondelete='CASCADE'), nullable=False)


class MenuModel(BaseModel):
    id: UUID4
    title: str
    description: str


class MenuDetailModel(MenuModel):
    submenus_count: int
    dishes_count: int


class SubmenuModel(BaseModel):
    id: UUID4
    title: str
    description: str
    menu_id: UUID4


class SubmenuDetailModel(SubmenuModel):
    dishes_count: int


class DishModel(BaseModel):
    id: UUID4
    title: str
    description: str
    price: decimal.Decimal
    submenu_id: UUID4
