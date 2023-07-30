import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from starlette.testclient import TestClient

from src.main import app

DATA_MENU = {'id': '01d46c92-fc19-4c5d-9417-2c3890e25a72',
             'title': 'Title', 'description': 'Description'
             }
DATA_MENU_UPDATE = {'title': 'Title update',
                    'description': 'Description update'
                    }

DATA_SUBMENU = {'id': 'ebae19d0-8cda-4f55-902b-e3d6a0bd6747',
                'title': 'Title', 'description': 'Description',
                'menu_id': '01d46c92-fc19-4c5d-9417-2c3890e25a72'
                }
DATA_SUBMENU_UPDATE = {'title': 'Title update',
                       'description': 'Description update'
                       }

DATA_DISH = {'id': '2cfb78d8-cb8d-4e65-b2d9-87c74c08a082',
             'title': 'Title',
             'description': 'Description',
             'price': '5.20',
             'submenu_id': 'ebae19d0-8cda-4f55-902b-e3d6a0bd6747'
             }
DATA_DISH_UPDATE = {'title': 'Title update',
                    'description': 'Description update',
                    'price': '14.50'
                    }


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8888/api/v1") as client:
        yield client
