from typing import Any

from ...api import APIError
from ..context import AppContext
from .base import Screen
from .builder import builder


def register_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    screen: Screen[dict[str, Any]] = (
        builder.add_main_header("Не авторизований користувач")
        .add_menu_header("Меню реєстрації нового користувача")
        .add_input_component(
            {
                "first_name": "Ваше ім'я: ",
                "last_name": "Ваше прізвище: ",
                "email": "Введіть email: ",
                "password": "Введіть пароль: ",
            }
        )
        .build(context)
    )
    user_data = screen.show()
    try:
        context.api.register(user_data)
    except APIError as e:
        print(e)
        input("Натисніть Enter, щоб продовжити ...")
    return "menu_unauth", {}
