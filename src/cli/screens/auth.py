from typing import Any

from ...api import APIError
from ..context import AppContext
from .builder import builder


def auth_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    screen = (
        builder.add_main_header("Не авторизований користувач")
        .add_input_component(
            {"username": "Введіть email: ", "password": "Введіть пароль: "}
        )
        .build(context)
    )
    user_data = screen.show()
    try:
        print(user_data)
        context.login(user_data)
    except APIError as e:
        print(e)
    return "main_menu", {}
