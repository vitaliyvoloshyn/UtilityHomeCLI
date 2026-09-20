# screens/menu.py
from InquirerPy import inquirer
from rich.console import Console
from rich.panel import Panel

from .base import BaseScreen

console = Console()


class MainMenuScreen(BaseScreen):
    def render(self) -> str:
        console.print(
            Panel("[bold cyan]🏡 Облік комунальних послуг[/bold cyan]", expand=False)
        )
        console.print(f"[bold green]Вітаємо, {self.context.username}[/bold green]\n")

        choice = inquirer.select(
            message="Оберіть дію:",
            choices=[
                {"name": "Переглянути таблицю даних", "value": "data_table"},
                {"name": "Вийти з акаунту", "value": "logout"},
                {"name": "Закрити програму", "value": "exit"},
            ],
        ).execute()

        return choice  # Поверне "data_table"
