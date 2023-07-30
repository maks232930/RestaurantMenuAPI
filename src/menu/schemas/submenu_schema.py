import uuid
from typing import Optional

from pydantic import BaseModel


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    id: Optional[uuid.UUID] = None


class SubmenuUpdate(SubmenuBase):
    pass
