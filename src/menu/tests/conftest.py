import asyncio
from asyncio import AbstractEventLoop
from typing import Any, AsyncGenerator, Generator

import pytest
from httpx import AsyncClient

from src.main import app

DATA_MENU: dict = {'id': '01d46c92-fc19-4c5d-9417-2c3890e25a72',
                   'title': 'Title', 'description': 'Description'
                   }
DATA_MENU_UPDATE: dict = {'title': 'Title update',
                          'description': 'Description update'
                          }

DATA_SUBMENU: dict = {'id': 'ebae19d0-8cda-4f55-902b-e3d6a0bd6747',
                      'title': 'Title', 'description': 'Description',
                      'menu_id': '01d46c92-fc19-4c5d-9417-2c3890e25a72'
                      }
DATA_SUBMENU_UPDATE: dict = {'title': 'Title update',
                             'description': 'Description update'
                             }

DATA_DISH: dict = {'id': '2cfb78d8-cb8d-4e65-b2d9-87c74c08a082',
                   'title': 'Title',
                   'description': 'Description',
                   'price': '5.20',
                   'submenu_id': 'ebae19d0-8cda-4f55-902b-e3d6a0bd6747'
                   }
DATA_DISH_UPDATE: dict = {'title': 'Title update',
                          'description': 'Description update',
                          'price': '14.50'
                          }


@pytest.fixture(scope='session')
def event_loop(request) -> Generator[AbstractEventLoop, Any, None]:
    """Create an instance of the default event loop for each test case."""
    loop: AbstractEventLoop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8888/api/v1') as client:
        yield client
