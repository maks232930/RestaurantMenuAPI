from sqlalchemy.orm import Session

from src.menu.models.dish_model import DishModel
from src.menu.models.menu_model import MenuModel
from src.menu.models.submenu_model import SubmenuModel
from src.menu.worker.tasks.utils_for_sync_excel.database_queries import (
    create_dish,
    create_menu,
    create_submenu,
    update_dish,
    update_menu,
    update_submenu,
)


def check_menu_data(menu_data_online: list[MenuModel], menu_data_offline: list[MenuModel], session: Session) -> None:
    for offline_menu in menu_data_offline:
        found: bool = False
        for online_menu in menu_data_online:
            if offline_menu.id == online_menu.id:
                found = True
                if offline_menu != online_menu:
                    update_menu(session, online_menu, offline_menu)
                break
        if not found:
            create_menu(session, offline_menu)


def check_submenu_data(submenu_data_online: list[SubmenuModel], submenu_data_offline: list[SubmenuModel],
                       session: Session) -> None:
    for offline_submenu in submenu_data_offline:
        found: bool = False
        for online_submenu in submenu_data_online:
            if offline_submenu.id == online_submenu.id:
                found = True
                if offline_submenu != online_submenu:
                    update_submenu(session, offline_submenu)
                break
        if not found:
            create_submenu(session, offline_submenu)


def check_dish_data(dish_data_online: list[DishModel], dish_data_offline: list[DishModel], session: Session) -> None:
    for offline_dish in dish_data_offline:
        found: bool = False
        for online_dish in dish_data_online:
            if offline_dish.id == online_dish.id:
                found = True
                if offline_dish != online_dish:
                    update_dish(session, offline_dish)
                break
        if not found:
            create_dish(session, offline_dish)
