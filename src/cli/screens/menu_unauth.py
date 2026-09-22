from ..context import AppContext
from .builder import builder


def menu_unauth_screen(context: AppContext):
    screen = (
        builder.add_main_header("не авторизований користувач")
        .add_choice_menu(
            [
                {"name": "Авторизуватися", "value": "login"},
                {"name": "Зареєструватися", "value": "register"},
            ],
            False,
        )
        .build(context)
    )
    action = screen.show()
    return action
