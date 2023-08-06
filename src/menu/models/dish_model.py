import uuid
from decimal import Decimal

from pydantic import UUID4, BaseModel
from sqlalchemy import UUID, Column, ForeignKey, Numeric, String

from src.database import Base


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    submenu_id = Column(UUID, ForeignKey('submenu.id', ondelete='CASCADE'), nullable=False)


class DishModel(BaseModel):
    id: UUID4
    title: str
    description: str
    price: Decimal
    submenu_id: UUID4
