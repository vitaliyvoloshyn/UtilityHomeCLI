from ..context import AppContext
from .builder import builder


def main_menu_screen(context: AppContext):
    properties = context.properties
    print(properties)

    screen = (
        builder
        .add_main_header(context.username)
        .add_choice_menu(
            [
                {"name": "Item1", "value": "dev"},
                {"name": "Item2", "value": "dev"},
            ]
        )
        .build(context)
    )
    action = screen.show()
    return action
