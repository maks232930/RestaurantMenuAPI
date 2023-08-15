from src.menu.worker.celery_app import redis_connection
from src.menu.worker.tasks.utils_for_sync_excel.database_queries import (
    create_dish,
    create_menu,
    create_submenu,
    update_dish,
    update_menu,
    update_submenu,
)


class CacheRedis:
    def __init__(self):
        self.redis = redis_connection

    def delete_cache(self, cache_keys: list[str]):
        with self.redis as redis:
            redis.unlink(*cache_keys, 'get_full_menu')


def create_menu_service(session, offline_menu, cache: CacheRedis = CacheRedis()):
    cache.delete_cache(['get_menus'])
    create_menu(session, offline_menu)


def update_menu_service(session, offline_menu, cache: CacheRedis = CacheRedis()):
    cache.delete_cache(['get_menus',
                        f'menu:{offline_menu.id}'])
    update_menu(session, offline_menu)


def update_submenu_service(session, offline_submenu, cache: CacheRedis = CacheRedis()):
    cache.delete_cache([
        f'get_submenus:{offline_submenu.menu_id}',
        f'menu:{offline_submenu.menu_id}:submenu:{offline_submenu.id}'
    ])
    update_submenu(session, offline_submenu)


def create_submenu_service(session, offline_submenu, cache: CacheRedis = CacheRedis()):
    cache.delete_cache([
        f'menu:{offline_submenu.menu_id}',
        f'get_submenus:{offline_submenu.menu_id}'
    ])
    create_submenu(session, offline_submenu)


def update_dish_service(session, offline_dish, cache: CacheRedis = CacheRedis()):
    cache.delete_cache([
        f'get_dishes:{offline_dish[1]}:{offline_dish[0].submenu_id}',
        f'menu:{offline_dish[1]}:submenu:{offline_dish[0].submenu_id}:dish:{offline_dish[0].id}'])
    update_dish(session, offline_dish[0])


def create_dish_service(session, offline_dish, cache: CacheRedis = CacheRedis()):
    cache.delete_cache([
        f'menu:{offline_dish[1]}',
        f'menu:{offline_dish[1]}:submenu:{offline_dish[0].submenu_id}',
        f'get_dishes:{offline_dish[1]}:{offline_dish[0].submenu_id}'
    ])
    create_dish(session, offline_dish[0])
