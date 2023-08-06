import pytest

from src.menu.tests.conftest import DATA_MENU, DATA_MENU_UPDATE


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
