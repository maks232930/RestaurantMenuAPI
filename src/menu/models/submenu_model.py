import uuid

from pydantic import UUID4, BaseModel
from sqlalchemy import UUID, Column, ForeignKey, String

from src.database import Base


class Submenu(Base):
    __tablename__ = 'submenu'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(UUID, ForeignKey('menu.id', ondelete='CASCADE'), nullable=False, unique=True)


class SubmenuModel(BaseModel):
    id: UUID4
    title: str
    description: str
    menu_id: UUID4


class SubmenuDetailModel(SubmenuModel):
    dishes_count: int
