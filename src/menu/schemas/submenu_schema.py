from uuid import UUID

from pydantic import BaseModel


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    id: UUID | None = None


class SubmenuUpdate(SubmenuBase):
    pass
