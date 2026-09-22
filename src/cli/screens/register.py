from ...api import APIError
from ..context import AppContext
from .builder import builder


def register_screen(context: AppContext):
    screen = (
        builder.add_main_header("Не авторизований користувач")
        .add_input_component(
            {
                "first_name": "Ваше ім'я: ",
                "last_name": "Ваше прізвище: ",
                "email": "Введіть email: ",
                "password": "Введіть пароль: "
            }
        )
        .build(context)
    )
    user_data = screen.show()
    try:
        context.api.register(user_data)
    except APIError as e:
        print(e)
    return "menu_unauth"
