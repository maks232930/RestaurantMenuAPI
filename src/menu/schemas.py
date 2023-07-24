from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


class SubmenuBase(BaseModel):
    title: str
    description: str


class SubmenuCreate(SubmenuBase):
    pass


class SubmenuUpdate(SubmenuBase):
    pass


class DishBase(BaseModel):
    title: str
    description: str
    price: float


class DishCreate(DishBase):
    pass


class DishUpdate(DishBase):
    pass
