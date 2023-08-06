from fastapi import FastAPI

from src.menu.api.dish_api import router as router_dish
from src.menu.api.menu_api import router as router_menu
from src.menu.api.submenu_api import router as router_submenu

app = FastAPI()

app.include_router(router_menu)
app.include_router(router_submenu)
app.include_router(router_dish)
