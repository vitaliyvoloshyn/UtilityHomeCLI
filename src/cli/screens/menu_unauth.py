# screens/auth.py
from InquirerPy import inquirer
from rich.console import Console

from ..context import AppContext
from .base import Screen
from .builder import builder

console = Console()


class MenuUnauthorized(Screen):
    def render(self) -> str:
        choice = inquirer.select(
            message="Оберіть дію:",
            choices=[
                {"name": "Ввійти в акаунт", "value": "auth"},
                {"name": "Зареєструватися", "value": "register"},
                {"name": "Закрити програму", "value": "exit"},
            ],
        ).execute()
        return choice


def menu_unauth_screen(context: AppContext):
    screen = (
        builder.add_main_header("не авторизований користувач")
        .add_choice_menu(
            [
                {"name": "Авторизуватися", "value": "login"},
                {"name": "Зареєструватися", "value": "registr"},
            ],
            False,
        )
        .build(context)
    )
    action = screen.show()
    return action
