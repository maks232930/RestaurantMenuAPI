import uuid

from pydantic import BaseModel, UUID4
from sqlalchemy import Column, String, UUID

from src.database import Base


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)


class MenuModel(BaseModel):
    id: UUID4
    title: str
    description: str


class MenuDetailModel(MenuModel):
    submenus_count: int
    dishes_count: int
