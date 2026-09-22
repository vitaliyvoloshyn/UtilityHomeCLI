# screens/menu.py
from InquirerPy import inquirer
from rich.console import Console
from rich.panel import Panel

from ..context import AppContext
from .base import Screen
from .builder import builder

console = Console()


class MainMenuScreen(Screen):
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


def main_menu_screen(context: AppContext):
    screen = (
        builder.add_main_header(context.username)
        .add_choice_menu(
            [
                {"name": "Item1", "value": "test"},
                {"name": "Item2", "value": "test"},
            ]
        )
        .build()
    )
    action = screen.show()
    return action
