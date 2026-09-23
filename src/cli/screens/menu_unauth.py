from ..context import AppContext
from .builder import builder


def menu_unauth_screen(context: AppContext):
    screen = (
        builder.add_main_header("не авторизований користувач")
        .add_menu_header("Стартове меню")
        .add_choice_menu(
            [
                {"name": "🔑 Авторизуватися", "value": "login"},
                {"name": "📝 Зареєструватися", "value": "register"},
            ],
            add_logout_exit_items=False,
            include_back_to_main_menu=False,
        )
        .build(context)
    )
    action = screen.show()
    return action
