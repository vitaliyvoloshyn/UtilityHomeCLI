# screens/auth.py
from InquirerPy import inquirer
from rich.console import Console

from ...api import APIError
from ..context import AppContext
from .base import Screen
from .builder import builder
from .components import InputComponent

console = Console()


class AuthScreen(Screen):
    def render(self) -> str:

        # Використовуємо inquirerpy для вводу
        email = inquirer.text(message="Введіть email:").execute()
        password = inquirer.secret(message="Введіть пароль:").execute()
        try:
            self.context.login({"username": email, "password": password})
        except APIError as e:
            print(e)
            return "auth"
        return "main_menu"


def auth_screen(context: AppContext):
    screen = (
        builder.add_main_header("Не авторизований користувач")
        .add_input_component(
            {"email": "Введіть email: ", "password": "Введіть пароль: "}
        )
        .build(context)
    )
    user_data = screen.show()
    try:
        context.login(user_data)
    except APIError as e:
        print(e)
        return "auth"
    return "main_menu"
