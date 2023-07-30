import pytest

from conftest import DATA_MENU, DATA_SUBMENU, DATA_DISH, DATA_DISH_UPDATE


@pytest.mark.asyncio
async def test_create_dish(client):
    await client.post("/menus", json=DATA_MENU)
    await client.post(f'/menus/{DATA_MENU["id"]}/submenus', json=DATA_SUBMENU)
    response = await client.post(f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}/dishes',
                                 json=DATA_DISH)

    response_json = response.json()

    assert response.status_code == 201
    assert response_json['id'] == DATA_DISH['id']
    assert response_json['title'] == DATA_DISH['title']
    assert response_json['description'] == DATA_DISH['description']
    assert response_json['submenu_id'] == DATA_DISH['submenu_id']


@pytest.mark.asyncio
async def test_get_dishes(client):
    response = await client.get(f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}/dishes')
    response_json = response.json()

    assert response.status_code == 200
    assert response_json[0]['id'] == DATA_DISH['id']
    assert response_json[0]['title'] == DATA_DISH['title']
    assert response_json[0]['description'] == DATA_DISH['description']
    assert response_json[0]['submenu_id'] == DATA_DISH['submenu_id']


@pytest.mark.asyncio
async def test_get_dish(client):
    response = await client.get(
        f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}/dishes/{DATA_DISH["id"]}')
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['id'] == DATA_DISH['id']
    assert response_json['title'] == DATA_DISH['title']
    assert response_json['description'] == DATA_DISH['description']
    assert response_json['submenu_id'] == DATA_DISH['submenu_id']


@pytest.mark.asyncio
async def test_patch_dish(client):
    response = await client.patch(
        f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}/dishes/{DATA_DISH["id"]}',
        json=DATA_DISH_UPDATE)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['title'] == DATA_DISH_UPDATE['title']
    assert response_json['description'] == DATA_DISH_UPDATE['description']
    assert response_json['price'] == DATA_DISH_UPDATE['price']


@pytest.mark.asyncio
async def test_delete_dish(client):
    await client.delete(f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}/dishes/{DATA_DISH["id"]}')
    await client.delete(f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}')
    await client.delete(f'/menus/{DATA_SUBMENU["menu_id"]}')

    response_dish = await client.get(
        f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}/dishes/{DATA_DISH["id"]}')
    response_menu = await client.get(f'/menus/{DATA_SUBMENU["menu_id"]}')
    response_submenu = await client.get(f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}')

    assert response_dish.status_code == 404
    assert response_menu.status_code == 404
    assert response_submenu.status_code == 404
