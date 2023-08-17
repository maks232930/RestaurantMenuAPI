import os
from typing import Any

import openpyxl

from src.database import SessionSync
from src.menu.worker.celery_app import celery_app
from src.menu.worker.tasks.utils_for_sync_excel.check_data import (
    check_dish_data,
    check_menu_data,
    check_submenu_data,
)
from src.menu.worker.tasks.utils_for_sync_excel.database_queries import (
    get_custom_full_menu,
)
from src.menu.worker.tasks.utils_for_sync_excel.parse_excel import parse_workbook
from src.menu.worker.tasks.utils_for_sync_excel.utils import ensure_directory_exists


@celery_app.task
def sync_excel_to_db():
    try:
        wb: Any = openpyxl.load_workbook('src/menu/admin/Menu.xlsx')
        sheet: Any = wb.active
        menu_data_offline, submenu_data_offline, dish_data_offline = parse_workbook(sheet)

        if len(menu_data_offline) + len(submenu_data_offline) + len(dish_data_offline) == 0:
            return 'Файл пустой'

        with SessionSync() as session:
            menu_data_online, submenu_data_online, dish_data_online = get_custom_full_menu(session=session)

            check_menu_data(menu_data_online, menu_data_offline, session=session)
            check_submenu_data(submenu_data_online, submenu_data_offline, session=session)
            check_dish_data(dish_data_online, dish_data_offline, session=session)

    except FileNotFoundError:
        repr('Файл не найден!')
        directory_path: str = 'src/menu/admin'
        ensure_directory_exists(directory_path)
        open(os.path.join(directory_path, 'Menu.xlsx'), 'w')
