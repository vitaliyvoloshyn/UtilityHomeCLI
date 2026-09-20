# screens/auth.py
from InquirerPy import inquirer
from rich.console import Console

from ...api import APIError
from .base import BaseScreen

console = Console()


class AuthScreen(BaseScreen):
    def render(self) -> str:
        choice = inquirer.select(
            message="Оберіть дію:",
            choices=[
                {"name": "Ввійти в акаунт", "value": "auth"},
                {"name": "Вийти з акаунту", "value": "logout"},
                {"name": "Закрити програму", "value": "exit"},
            ],
        ).execute()
        return choice

        # Використовуємо inquirerpy для вводу
        email = inquirer.text(message="Введіть email:").execute()
        password = inquirer.secret(message="Введіть пароль:").execute()
        try:
            self.context.login({"username": email, "password": password})
        except APIError as e:
            print(e)
            return "auth"
        return "main_menu"
