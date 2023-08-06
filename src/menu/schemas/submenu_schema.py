import uuid

from pydantic import BaseModel


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    id: uuid.UUID | None = None


class SubmenuUpdate(SubmenuBase):
    pass
