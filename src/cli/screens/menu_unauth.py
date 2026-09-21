# screens/auth.py
from InquirerPy import inquirer
from rich.console import Console

from ...api import APIError
from .base import BaseScreen

console = Console()


class MenuUnauthorized(BaseScreen):
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
