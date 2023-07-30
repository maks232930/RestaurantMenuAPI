import uuid
from typing import Optional

from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    id: Optional[uuid.UUID] = None


class MenuUpdate(MenuBase):
    pass
