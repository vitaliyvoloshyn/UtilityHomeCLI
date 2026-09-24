from typing import Any

from ..context import AppContext
from .builder import builder


def dev_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    screen = (
        builder.add_main_header(context.username)
        .add_text_label("Даний пункт меню знаходиться у розробці ... 🚧")
        .add_choice_menu([])
        .build(context)
    )
    action = screen.show()
    return action, {}
