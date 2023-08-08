from uuid import UUID

from pydantic import BaseModel


class DishBase(BaseModel):
    title: str
    description: str
    price: float


class DishCreate(DishBase):
    id: UUID | None = None


class DishUpdate(DishBase):
    pass
