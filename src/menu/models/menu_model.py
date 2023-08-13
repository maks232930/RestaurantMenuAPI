import uuid

from pydantic import UUID4, BaseModel
from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import relationship

from src.database import Base


class Menu(Base):
    __tablename__ = 'menu'

    id: UUID4 = Column(UUID, primary_key=True, default=uuid.uuid4)
    title: str = Column(String, nullable=False, unique=True)
    description: str = Column(String, nullable=False)

    submenus = relationship('Submenu', back_populates='menu')


class MenuModel(BaseModel):
    id: UUID4
    title: str
    description: str


class MenuDetailModel(MenuModel):
    submenus_count: int
    dishes_count: int
