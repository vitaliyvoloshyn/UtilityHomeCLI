from .builder import builder
from ..context import AppContext


def error_screen(context: AppContext):
    screen = (
        builder
        .add_main_header(context.username)
        .add_text_label(context.error_message)
        .add_choice_menu(
            [
                {"name": "Повернутися в головне меню", "value": "main_menu"},
            ],
        )
        .build(context)
    )
    action = screen.show()
    return action
