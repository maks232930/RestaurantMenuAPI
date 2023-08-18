from typing import Sequence

from sqlalchemy import Result, Select, Update, select, update
from sqlalchemy.orm import Session, selectinload

from src.menu.models.dish_model import Dish, DishModel
from src.menu.models.menu_model import Menu, MenuModel
from src.menu.models.submenu_model import Submenu, SubmenuModel


def create_menu(session: Session, offline_menu: MenuModel) -> None:
    db_menu: Menu = Menu(**offline_menu.model_dump())
    session.add(db_menu)
    session.commit()
    session.refresh(db_menu)


def update_menu(session: Session, offline_menu: MenuModel) -> None:
    query: Update = update(Menu).where(Menu.id == offline_menu.id).values(**offline_menu.model_dump())
    session.execute(query)
    session.commit()


def update_submenu(session: Session, offline_submenu: SubmenuModel) -> None:
    query: Update = (
        update(Submenu)
        .where(
            Submenu.menu_id == offline_submenu.menu_id,
            Submenu.id == offline_submenu.id
        )
        .values(**offline_submenu.model_dump())
    )
    session.execute(query)
    session.commit()


def create_submenu(session: Session, offline_submenu: SubmenuModel) -> None:
    db_submenu: Submenu = Submenu(**offline_submenu.model_dump())
    session.add(db_submenu)
    session.commit()
    session.refresh(db_submenu)


def update_dish(session: Session, offline_dish: DishModel) -> None:
    query: Update = (
        update(Dish)
        .where(Dish.id == offline_dish.id)
        .values(**offline_dish.model_dump())
    )
    session.execute(query)
    session.commit()


def create_dish(session: Session, offline_dish: DishModel) -> None:
    db_dish: Dish = Dish(**offline_dish.model_dump())
    session.add(db_dish)
    session.commit()
    session.refresh(db_dish)


def get_custom_full_menu(session: Session) -> tuple[list[MenuModel], list[SubmenuModel], list[DishModel]]:
    menu_query: Select = (
        select(Menu)
        .options(
            selectinload(Menu.submenus)
            .selectinload(Submenu.dishes)
        )
    )
    result: Result = session.execute(menu_query)
    menus: Sequence = result.scalars().all()

    menu_data: list[MenuModel] = []
    submenu_data: list[SubmenuModel] = []
    dish_data: list[DishModel] = []

    for menu in menus:
        menu_model: MenuModel = MenuModel(
            id=menu.id,
            title=menu.title,
            description=menu.description
        )
        menu_data.append(menu_model)

        for submenu in menu.submenus:
            submenu_model: SubmenuModel = SubmenuModel(
                id=submenu.id,
                title=submenu.title,
                description=submenu.description,
                menu_id=submenu.menu_id
            )
            submenu_data.append(submenu_model)

            for dish in submenu.dishes:
                dish_model: DishModel = DishModel(
                    id=dish.id,
                    title=dish.title,
                    description=dish.description,
                    price=dish.price,
                    submenu_id=submenu.id
                )
                dish_data.append(dish_model)

    return menu_data, submenu_data, dish_data
