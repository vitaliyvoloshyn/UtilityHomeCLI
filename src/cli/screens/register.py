# screens/auth.py
from InquirerPy import inquirer
from rich.console import Console

from ...api import APIError
from .base import Screen

console = Console()


class RegisterScreen(Screen):
    def render(self) -> str:

        # Використовуємо inquirerpy для вводу
        first_name = inquirer.text(message="Введіть своє імя:").execute()
        Last_name = inquirer.text(message="Введіть своє прізвище:").execute()
        email = inquirer.text(message="Введіть свій email:").execute()
        password = inquirer.secret(message="Придумайте пароль:").execute()
        try:
            self.context.api.register(
                {
                    "email": email,
                    "password": password,
                    "first_name": first_name,
                    "last_name": Last_name,
                }
            )
        except APIError as e:
            print(e)
            input("Натисніть Enter, щоб повернутися в попереднє меню...")

        return "menu_unauth"
