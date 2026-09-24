from typing import Any

from ..context import AppContext
from .builder import builder


def error_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    screen = (
        builder.add_main_header(context.username)
        .add_text_label(context.error_message)
        .add_choice_menu([])
        .build(context)
    )
    action = screen.show()
    return action, {}
