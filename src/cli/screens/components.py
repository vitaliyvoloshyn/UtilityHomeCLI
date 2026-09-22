from abc import ABC, abstractmethod
from datetime import UTC, datetime

from InquirerPy import inquirer
from rich.box import HEAVY
from rich.console import Console
from rich.panel import Panel

console = Console()


class BaseComponent(ABC):
    @abstractmethod
    def render(self):
        raise NotImplementedError


class HeaderComponent(BaseComponent):
    def render(self): ...


class MainHeader(BaseComponent):
    def __init__(self, username: str):
        self.username = username

    def render(self):
        # Комплексна велика панель із заголовками та кастомною рамкою
        styled_panel = Panel(
            f"Користувач: {self.username}\nПоточна дата - {datetime.now(UTC).date()}",
            title="[bold magenta]Система обліку комунальних послуг[/bold magenta]",
            title_align="left",
            subtitle="Версія 1.0.0",
            subtitle_align="right",
            box=HEAVY,
            border_style="yellow",
            padding=(1, 2),  # відступи (вертикальні, горизонтальні)
            expand=True,
        )
        console.print(styled_panel)


class LogoutExitMenu(BaseComponent):
    def render(self):
        choice = inquirer.select(
            message="Оберіть дію:",
            choices=[
                {"name": "Вийти з акаунту", "value": "logout"},
                {"name": "Закрити програму", "value": "exit"},
            ],
        ).execute()
        return choice


class ChoiceMenu(BaseComponent):
    def __init__(self, items: list[dict[str, str]], add_logout_exit_items: bool = True):
        self.items = items
        self.add_logout_exit_items = add_logout_exit_items

    def render(self):
        final_choices = self.items
        if self.add_logout_exit_items:
            final_choices.extend(
                [
                    {"name": "Вийти з акаунту", "value": "logout"},
                    {"name": "Закрити програму", "value": "exit"},
                ]
            )
        choice = inquirer.select(
            message="Оберіть дію:",
            choices=self.items,
        ).execute()
        return choice


class InputComponent(BaseComponent):
    def __init__(self, messages: dict[str, str]):
        self.messages = messages

    def parse_messages(self):
        for message in self.messages:
            self.__setattr__(message.keys(), message.values())

    def render(self):
        out_dict = self.messages.copy()
        for key, message in out_dict.items():
            out_dict[key] = inquirer.text(message=message).execute()
        return out_dict
