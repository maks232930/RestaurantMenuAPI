from decimal import Decimal
from typing import Any, Union
from uuid import UUID

from src.menu.models.dish_model import DishModel
from src.menu.models.menu_model import MenuModel
from src.menu.models.submenu_model import SubmenuModel


def is_valid_data(model: str, data: list) -> bool:
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


def is_valid_uuid(uuid_str):
    try:
        uuid_obj = UUID(uuid_str)
        return str(uuid_obj) == uuid_str
    except ValueError:
        return False
    except AttributeError:
        return False


def parse_workbook(sheet) -> tuple[list[MenuModel], list[SubmenuModel], list[Any]]:
    menu_data: list[MenuModel] = []
    submenu_data: list[SubmenuModel] = []
    dish_data: Any = []
    menu_id = None
    submenu_id = None

    for row in sheet.iter_rows(min_row=1, values_only=True):
        if row[0] is not None:
            if is_valid_uuid(row[0]):
                check_data = is_valid_data('menu', [row[0], row[1], row[2]])
                if check_data:
                    menu_id = UUID(row[0])
                    menu_data.append(MenuModel(id=menu_id, title=row[1], description=row[2]))
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
                            SubmenuModel(id=submenu_id, title=row[2], description=row[3], menu_id=menu_id))
                        continue
                continue
        if row[2] is not None:
            if is_valid_uuid(row[2]):
                if submenu_id != '':
                    check_data = is_valid_data('dish', [row[2], row[3], row[4], row[5], submenu_id])
                    if check_data:
                        dish_data.append(
                            [DishModel(id=UUID(row[2]), title=row[3], description=row[4], price=row[5],
                                       submenu_id=submenu_id),
                             menu_id
                             ])
    return menu_data, submenu_data, dish_data
