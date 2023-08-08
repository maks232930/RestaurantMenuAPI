from aioredis import from_url
from fastapi import FastAPI

from src.database import REDIS_URL
from src.menu.api.dish_api import router as router_dish
from src.menu.api.menu_api import router as router_menu
from src.menu.api.submenu_api import router as router_submenu

app = FastAPI()


@app.on_event('startup')
async def startup_event():
    async with await from_url(REDIS_URL) as redis:
        await redis.flushdb(asynchronous=True)


app.include_router(router_menu)
app.include_router(router_submenu)
app.include_router(router_dish)
