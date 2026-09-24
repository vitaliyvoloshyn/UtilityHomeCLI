from typing import Any

from ..context import AppContext
from .builder import builder


def login_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    screen = (
        builder.add_main_header("не авторизований користувач")
        .add_menu_header("Меню авторизації користувача")
        .add_input_component(
            {"email": "Введіть email: ", "password": "Введіть пароль: "}
        )
        .build(context)
    )
    action = screen.show()
    return action, {}
