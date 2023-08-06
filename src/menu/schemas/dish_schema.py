import uuid

from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: str
    price: float


class DishCreate(DishBase):
    id: uuid.UUID | None = None


class DishUpdate(DishBase):
    pass
