import pytest

from src.menu.tests.conftest import DATA_DISH, DATA_MENU, DATA_MENU_UPDATE, DATA_SUBMENU


@pytest.mark.asyncio
async def test_create_menu(test_client):
    response = await test_client.post('/menus', json=DATA_MENU)
    response_json = response.json()

    assert response.status_code == 201
    assert response_json['id'] == DATA_MENU['id']
    assert response_json['title'] == DATA_MENU['title']
    assert response_json['description'] == DATA_MENU['description']


@pytest.mark.asyncio
async def test_get_menus(test_client):
    response = await test_client.get('/menus')
    response_json = response.json()

    assert len(response_json) == 1
    assert response_json[0]['id'] == DATA_MENU['id']
    assert response_json[0]['title'] == DATA_MENU['title']
    assert response_json[0]['description'] == DATA_MENU['description']


@pytest.mark.asyncio
async def test_get_menu_detail(test_client):
    response = await test_client.get(f'/menus/{DATA_MENU["id"]}')
    response_json = response.json()

    assert response_json['id'] == DATA_MENU['id']
    assert response_json['title'] == DATA_MENU['title']
    assert response_json['description'] == DATA_MENU['description']
    assert response_json['submenus_count'] == 0
    assert response_json['dishes_count'] == 0


@pytest.mark.asyncio
async def test_get_full_menu(test_client):
    await test_client.post(f'/menus/{DATA_MENU["id"]}/submenus', json=DATA_SUBMENU)
    await test_client.post(f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}/dishes',
                           json=DATA_DISH)
    response = await test_client.get('/menus/full')
    response_json = response.json()

    assert response_json[0]['menu']['id'] == DATA_MENU['id']
    assert response_json[0]['menu']['title'] == DATA_MENU['title']
    assert response_json[0]['menu']['description'] == DATA_MENU['description']

    assert response_json[0]['menu']['submenus'][0]['id'] == DATA_SUBMENU['id']
    assert response_json[0]['menu']['submenus'][0]['title'] == DATA_SUBMENU['title']
    assert response_json[0]['menu']['submenus'][0]['description'] == DATA_SUBMENU['description']

    assert response_json[0]['menu']['submenus'][0]['dishes'][0]['id'] == DATA_DISH['id']
    assert response_json[0]['menu']['submenus'][0]['dishes'][0]['title'] == DATA_DISH['title']
    assert response_json[0]['menu']['submenus'][0]['dishes'][0]['description'] == DATA_DISH['description']
    assert response_json[0]['menu']['submenus'][0]['dishes'][0]['price'] == DATA_DISH['price']


@pytest.mark.asyncio
async def test_patch_menu(test_client):
    response = await test_client.patch(f'/menus/{DATA_MENU["id"]}', json=DATA_MENU_UPDATE)
    response_json = response.json()

    assert response_json['title'] == DATA_MENU_UPDATE['title']
    assert response_json['description'] == DATA_MENU_UPDATE['description']


@pytest.mark.asyncio
async def test_delete_menu(test_client):
    await test_client.delete(f'/menus/{DATA_MENU["id"]}')
    response = await test_client.get(f'/menus/{DATA_MENU["id"]}')

    assert response.status_code == 404
