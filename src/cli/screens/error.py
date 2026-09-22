# screens/menu.py
from InquirerPy import inquirer
from rich.console import Console

from .base import Screen

console = Console()


class APIErrorScreen(Screen):
    def render(self) -> str:
        console.print(f"[bold red]{self.context.error_message}[/bold red]\n")

        return "exit"
