from .builder import builder
from ..context import AppContext


def dev_screen(context: AppContext):
    screen = (
        builder
        .add_main_header(context.username)
        .add_text_label("Даний пункт меню знаходиться у розробці ... 🚧")
        .add_choice_menu([])
        .build(context)
    )
    action = screen.show()
    return action
