import pytest
from httpx import AsyncClient, Response

from src.menu.tests.conftest import DATA_MENU, DATA_SUBMENU, DATA_SUBMENU_UPDATE


@pytest.mark.asyncio
async def test_create_submenu(test_client: AsyncClient):
    await test_client.post('/menus', json=DATA_MENU)
    response: Response = await test_client.post(f'/menus/{DATA_MENU["id"]}/submenus', json=DATA_SUBMENU)
    response_json: dict = response.json()

    assert response.status_code == 201
    assert response_json['id'] == DATA_SUBMENU['id']
    assert response_json['title'] == DATA_SUBMENU['title']
    assert response_json['description'] == DATA_SUBMENU['description']
    assert response_json['menu_id'] == DATA_SUBMENU['menu_id']


@pytest.mark.asyncio
async def test_get_submenus(test_client: AsyncClient):
    response: Response = await test_client.get(f'/menus/{DATA_SUBMENU["menu_id"]}/submenus')
    response_json: dict = response.json()

    assert response.status_code == 200
    assert len(response_json) == 1
    assert response_json[0]['id'] == DATA_SUBMENU['id']
    assert response_json[0]['title'] == DATA_SUBMENU['title']
    assert response_json[0]['description'] == DATA_SUBMENU['description']
    assert response_json[0]['menu_id'] == DATA_SUBMENU['menu_id']


@pytest.mark.asyncio
async def test_get_submenu_detail(test_client: AsyncClient):
    response: Response = await test_client.get(f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}')
    response_json: dict = response.json()

    assert response.status_code == 200
    assert response_json['id'] == DATA_SUBMENU['id']
    assert response_json['title'] == DATA_SUBMENU['title']
    assert response_json['description'] == DATA_SUBMENU['description']
    assert response_json['dishes_count'] == 0


@pytest.mark.asyncio
async def test_patch_submenu(test_client: AsyncClient):
    response: Response = await test_client.patch(f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}',
                                                 json=DATA_SUBMENU_UPDATE)
    response_json: dict = response.json()

    assert response.status_code == 200
    assert response_json['title'] == DATA_SUBMENU_UPDATE['title']
    assert response_json['description'] == DATA_SUBMENU_UPDATE['description']


@pytest.mark.asyncio
async def test_delete_submenu(test_client: AsyncClient):
    await test_client.delete(f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}')
    await test_client.delete(f'/menus/{DATA_SUBMENU["menu_id"]}')

    response_menu: Response = await test_client.get(f'/menus/{DATA_SUBMENU["menu_id"]}')
    response_submenu: Response = await test_client.get(
        f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}')

    assert response_menu.status_code == 404
    assert response_submenu.status_code == 404
