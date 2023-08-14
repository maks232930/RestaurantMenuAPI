import logging
import os

import openpyxl

from src.menu.worker.celery_app import celery_app
from src.menu.worker.tasks.utils import (
    check_dish_data,
    check_menu_data,
    check_submenu_data,
    get_custom_full_menu,
    parse_workbook,
)

logging.basicConfig(level=logging.INFO)


@celery_app.task
async def sync_excel_to_db():
    try:
        logging.info('0')
        wb = openpyxl.load_workbook('src/menu/admin/Menu.xlsx')
        logging.info('1')
        sheet = wb.active
        logging.info('2')
        menu_data_offline, submenu_data_offline, dish_data_offline = parse_workbook(sheet)
        logging.info('Starting excel_sync_task')
        logging.info('menu_data_offline: %s', menu_data_offline)
        logging.info('submenu_data_offline: %s', submenu_data_offline)
        logging.info('dish_data_offline: %s', dish_data_offline)

        if len(menu_data_offline) + len(submenu_data_offline) + len(dish_data_offline) == 0:
            return 'Файл пустой'

        logging.info('Fetching menu data from the database')
        menu_data_online, submenu_data_online, dish_data_online = await get_custom_full_menu()

        logging.info('menu_data_online: %s', menu_data_online)
        logging.info('submenu_data_online: %s', submenu_data_online)
        logging.info('dish_data_online: %s', dish_data_online)

        await check_menu_data(menu_data_online, menu_data_offline)
        await check_submenu_data(submenu_data_online, submenu_data_offline)
        await check_dish_data(dish_data_online, dish_data_offline)

    except FileNotFoundError:
        logging.info('Файл не найден')
        open(os.path.join('src/menu/admin', 'Menu.xlsx'), 'w')
