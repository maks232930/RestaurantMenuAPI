import uuid
from typing import Optional

from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: str
    price: float


class DishCreate(DishBase):
    id: Optional[uuid.UUID] = None


class DishUpdate(DishBase):
    pass
