from fastapi import FastAPI

from src.menu.router import router as router_menu

app = FastAPI()

app.include_router(router_menu)
