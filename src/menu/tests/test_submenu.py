import pytest

from conftest import DATA_MENU, DATA_SUBMENU, DATA_SUBMENU_UPDATE


@pytest.mark.asyncio
async def test_create_submenu(client):
    await client.post('/menus', json=DATA_MENU)
    response = await client.post(f'/menus/{DATA_MENU["id"]}/submenus', json=DATA_SUBMENU)
    response_json = response.json()

    assert response.status_code == 201
    assert response_json['id'] == DATA_SUBMENU['id']
    assert response_json['title'] == DATA_SUBMENU['title']
    assert response_json['description'] == DATA_SUBMENU['description']
    assert response_json['menu_id'] == DATA_SUBMENU['menu_id']


@pytest.mark.asyncio
async def test_get_submenus(client):
    response = await client.get(f'/menus/{DATA_SUBMENU["menu_id"]}/submenus')
    response_json = response.json()

    assert response.status_code == 200
    assert len(response_json) == 1
    assert response_json[0]['id'] == DATA_SUBMENU['id']
    assert response_json[0]['title'] == DATA_SUBMENU['title']
    assert response_json[0]['description'] == DATA_SUBMENU['description']
    assert response_json[0]['menu_id'] == DATA_SUBMENU['menu_id']


@pytest.mark.asyncio
async def test_get_submenu_detail(client):
    response = await client.get(f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}')
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['id'] == DATA_SUBMENU['id']
    assert response_json['title'] == DATA_SUBMENU['title']
    assert response_json['description'] == DATA_SUBMENU['description']
    assert response_json['dishes_count'] == 0


@pytest.mark.asyncio
async def test_patch_submenu(client):
    response = await client.patch(f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}',
                                  json=DATA_SUBMENU_UPDATE)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['title'] == DATA_SUBMENU_UPDATE['title']
    assert response_json['description'] == DATA_SUBMENU_UPDATE['description']



@pytest.mark.asyncio
async def test_delete_submenu(client):
    await client.delete(f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}')
    await client.delete(f'/menus/{DATA_SUBMENU["menu_id"]}')

    response_menu = await client.get(f'/menus/{DATA_SUBMENU["menu_id"]}')
    response_submenu = await client.get(f'/menus/{DATA_SUBMENU["menu_id"]}/submenus/{DATA_SUBMENU["id"]}')

    assert response_menu.status_code == 404
    assert response_submenu.status_code == 404
