import uuid
from decimal import Decimal

from pydantic import UUID4, BaseModel
from sqlalchemy import UUID, Column, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship

from src.database import Base


class Dish(Base):
    __tablename__ = 'dish'

    id: UUID4 = Column(UUID, primary_key=True, default=uuid.uuid4)
    title: str = Column(String, nullable=False, unique=True)
    description: str = Column(String, nullable=False)
    price: float = Column(Numeric(precision=10, scale=2), nullable=False)
    submenu_id: UUID4 = Column(UUID, ForeignKey('submenu.id', ondelete='CASCADE'), nullable=False)

    submenu = relationship('Submenu', back_populates='dishes')


class DishModel(BaseModel):
    id: UUID4
    title: str
    description: str
    price: Decimal
    submenu_id: UUID4
