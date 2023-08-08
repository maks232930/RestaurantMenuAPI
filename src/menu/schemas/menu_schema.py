from uuid import UUID

from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    id: UUID | None = None


class MenuUpdate(MenuBase):
    pass
