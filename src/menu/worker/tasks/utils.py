from decimal import Decimal
from typing import Any, Union
from uuid import UUID

import httpx
from fastapi import Depends
from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database import get_async_session
from src.menu.models.dish_model import CustomDishModel, DishModel
from src.menu.models.menu_model import Menu, MenuModel
from src.menu.models.submenu_model import Submenu, SubmenuModel

BASE_URL = 'http://web:8000/api/v1/'


async def is_valid_data(model: str, data: list) -> bool:
    if model == 'menu':
        expected_types_menu: list[Any] = [UUID, str, str]
        for index, item in enumerate(data):
            if item == '' and not isinstance(item, expected_types_menu[index]):
                return False
        return True
    elif model == 'submenu':
        expected_types_submenu: list[Any] = [UUID, str, str, UUID]
        for index, item in enumerate(data):
            if item == '' and not isinstance(item, expected_types_submenu[index]):
                return False
        return True
    elif model == 'dish':
        expected_types_dish: list[Any] = [UUID, str, str, Union[Decimal, int, float], UUID]
        for index, item in enumerate(data):
            if item == '' and not isinstance(item, expected_types_dish[index]):
                return False
        return True
    return False


async def is_valid_uuid(uuid_str):
    try:
        uuid_obj = UUID(uuid_str)
        return str(uuid_obj) == uuid_str
    except ValueError:
        return False


def parse_workbook(sheet):
    menu_data: list[MenuModel] = []
    submenu_data: list[SubmenuModel] = []
    dish_data: list[DishModel] = []
    menu_id = None
    submenu_id = None

    for row in sheet.iter_rows(min_row=1, values_only=True):
        if row[0] is not None:
            if is_valid_uuid(row[0]):
                check_data = is_valid_data('menu', [row[0], row[1], row[2]])
                if check_data:
                    menu_id = UUID(row[0])
                    menu_data.append(MenuModel(id=UUID(row[0]), title=row[1], description=row[2]))
                    continue
                else:
                    continue
        if row[1] is not None:
            if is_valid_uuid(row[1]):
                if menu_id != '':
                    check_data = is_valid_data('submenu', [row[1], row[2], row[3], menu_id])
                    if check_data:
                        submenu_id = UUID(row[1])
                        submenu_data.append(
                            SubmenuModel(id=UUID(row[1]), title=row[2], description=row[3], menu_id=menu_id))
                        continue
                continue
        if row[2] is not None:
            if is_valid_uuid(row[2]):
                if submenu_id != '':
                    check_data = is_valid_data('dish', [row[2], row[3], row[4], row[5], submenu_id])
                    if check_data:
                        dish_data.append(
                            CustomDishModel(id=UUID(row[2]), title=row[3], description=row[4], price=row[5],
                                            submenu_id=submenu_id, menu_id=menu_id))
    return menu_data, submenu_data, dish_data


async def get_custom_full_menu(session: AsyncSession = Depends(get_async_session)) \
        -> tuple[list[MenuModel], list[SubmenuModel], list[DishModel]]:
    menu_query: Select = (
        select(Menu)
        .options(
            selectinload(Menu.submenus)
            .selectinload(Submenu.dishes)
        )
    )
    result: Result = await session.execute(menu_query)
    menus = result.scalars().all()

    menu_data: list[MenuModel] = []
    submenu_data: list[SubmenuModel] = []
    dish_data: list[DishModel] = []

    for menu in menus:
        menu_model = MenuModel(
            id=menu.id,
            title=menu.title,
            description=menu.description
        )
        menu_data.append(menu_model)

        for submenu in menu.submenus:
            submenu_model = SubmenuModel(
                id=submenu.id,
                title=submenu.title,
                description=submenu.description,
                menu_id=submenu.menu_id
            )
            submenu_data.append(submenu_model)

            for dish in submenu.dishes:
                dish_model = DishModel(
                    id=dish.id,
                    title=dish.title,
                    description=dish.description,
                    price=dish.price,
                    submenu_id=submenu.id
                )
                dish_data.append(dish_model)

    return menu_data, submenu_data, dish_data


async def update_menu(menu: MenuModel):
    async with httpx.AsyncClient() as client:
        await client.patch(f'{BASE_URL}menus/{menu.id}', json=menu.model_dump_json())


async def create_menu(menu: MenuModel):
    async with httpx.AsyncClient() as client:
        await client.post(f'{BASE_URL}menus', json=menu.model_dump_json())


async def update_submenu(submenu: SubmenuModel):
    async with httpx.AsyncClient() as client:
        await client.patch(f'{BASE_URL}menus/{submenu.menu_id}/submenus/{submenu.id}', json=submenu.model_dump_json())


async def create_submenu(submenu: SubmenuModel):
    async with httpx.AsyncClient() as client:
        await client.post(f'{BASE_URL}menus/{submenu.menu_id}/submenus', json=submenu.model_dump_json())


async def update_dish(dish: CustomDishModel):
    async with httpx.AsyncClient() as client:
        request_data = DishModel(id=dish.id, title=dish.title, description=dish.description, price=dish.price,
                                 submenu_id=dish.submenu_id)
        await client.patch(f'{BASE_URL}menus/{dish.menu_id}/submenus/{dish.submenu_id}/dishes/{dish.id}',
                           json=request_data.model_dump_json())


async def create_dish(dish: CustomDishModel):
    async with httpx.AsyncClient() as client:
        request_data = DishModel(id=dish.id, title=dish.title, description=dish.description, price=dish.price,
                                 submenu_id=dish.submenu_id)
        await client.post(f'{BASE_URL}menus/{dish.menu_id}/submenus/{dish.submenu_id}/dishes/{dish.id}',
                          json=request_data.model_dump_json())


async def check_menu_data(menu_data_online: list[MenuModel], menu_data_offline: list[MenuModel]):
    for offline_menu in menu_data_offline:
        found: bool = False
        for online_menu in menu_data_online:
            if offline_menu.id == online_menu.id:
                found = True
                if offline_menu != online_menu:
                    await update_menu(offline_menu)
                break
        if not found:
            await create_menu(offline_menu)


async def check_submenu_data(submenu_data_online: list[SubmenuModel], submenu_data_offline: list[SubmenuModel]):
    for offline_submenu in submenu_data_offline:
        found: bool = False
        for online_submenu in submenu_data_online:
            if offline_submenu.id == online_submenu.id:
                found = True
                if offline_submenu != online_submenu:
                    await update_submenu(offline_submenu)
                break
        if not found:
            await create_submenu(offline_submenu)


async def check_dish_data(dish_data_online: list[DishModel], dish_data_offline: list[CustomDishModel]):
    for offline_dish in dish_data_offline:
        found: bool = False
        for online_dish in dish_data_online:
            if offline_dish.id == online_dish.id:
                found = True
                if offline_dish != online_dish:
                    await update_dish(offline_dish)
                break
        if not found:
            await create_dish(offline_dish)
