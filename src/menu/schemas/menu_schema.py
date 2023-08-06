import uuid

from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    id: uuid.UUID | None = None


class MenuUpdate(MenuBase):
    pass
