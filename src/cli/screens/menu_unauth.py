from typing import Any

from ..context import AppContext
from .builder import builder


def menu_unauth_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    screen = (
        builder.add_main_header("не авторизований користувач")
        .add_menu_header("Стартове меню")
        .add_choice_menu(
            [
                {"name": "🔑 Авторизуватися", "value": {"action": "login"}},
                {"name": "📝 Зареєструватися", "value": "register"},
            ],
            add_logout_exit_items=False,
            include_back_to_main_menu=False,
        )
        .build(context)
    )
    res = screen.show()
    action = res.get("action")
    if action is None:
        raise ValueError("action не знайдено")
    params = res.get("params") or {}
    return action, params
