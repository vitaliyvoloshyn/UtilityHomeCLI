from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import Any

from InquirerPy.prompts.input import InputPrompt
from InquirerPy.prompts.list import ListPrompt
from rich.box import HEAVY, ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ...api.models import AccountNumberResponse

console = Console()


class BaseComponent[T = str | dict[str, Any] | None](ABC):
    @abstractmethod
    def render(self) -> T:
        raise NotImplementedError


class MenuHeaderComponent(BaseComponent[None]):
    def __init__(self, title: str):
        self.title = title

    def render(self) -> None:
        styled_panel = Panel(
            self.title,
            box=ROUNDED,
            border_style="green",
            expand=False,
        )
        console.print(styled_panel)


class AppHeader(BaseComponent[None]):
    def __init__(self, username: str):
        self.username = username

    def render(self) -> None:
        # Комплексна велика панель із заголовками та кастомною рамкою
        styled_panel = Panel(
            f"Користувач: {self.username}\nПоточна дата - {datetime.now(UTC).date()}",
            title="[bold magenta]🏡  Система обліку комунальних послуг[/bold magenta]",
            title_align="left",
            subtitle="Версія 1.0.0",
            subtitle_align="right",
            box=HEAVY,
            border_style="yellow",
            padding=(1, 2),  # відступи (вертикальні, горизонтальні)
            expand=True,
        )
        console.print(styled_panel)


class ChoiceMenu(BaseComponent[str]):
    def __init__(
        self,
        items: list[dict[str, Any]],
        message: str = "Оберіть дію:",
        add_logout_exit_items: bool = True,
        include_back_to_main_menu: bool = True,
    ):
        self.message = message
        self.items = items
        self.add_logout_exit_items = add_logout_exit_items
        self.include_back_to_main_menu = include_back_to_main_menu

    def render(self) -> str:
        final_choices = self.items
        if self.add_logout_exit_items:
            final_choices.extend(
                [
                    {
                        "name": "↩️ Повернутися у попереднє меню",
                        "value": {"action": "prev_menu"},
                    },
                    {
                        "name": "🔙 Повернутися у головне меню",
                        "value": {"action": "main_menu"},
                    },
                    {"name": "🚪 Вийти з акаунту", "value": {"action": "logout"}},
                    {"name": "❌ Закрити програму", "value": {"action": "exit"}},
                ]
            )
        choice = ListPrompt(
            message=self.message,
            choices=final_choices,
        ).execute()
        return choice


class InputComponent(BaseComponent[dict]):
    def __init__(self, messages: dict[str, Any]):
        self.messages = messages

    def render(self) -> dict:
        out_dict = self.messages.copy()
        for key, message in out_dict.items():
            out_dict[key] = InputPrompt(message=message).execute()
        return {"payload": out_dict}


class TextLabel(BaseComponent[None]):
    def __init__(self, text: str):
        self.text = text

    def render(self) -> None:
        console.print(f"[bold green]{self.text}[/bold green]\n")


class TableAccountsList(BaseComponent[None]):
    def __init__(self, data: list[AccountNumberResponse]) -> None:
        self.data = data

    def total_balance(self) -> float:
        return sum(item.balance for item in self.data if item.balance < 0)

    def render(self) -> None:
        total_balance = self.total_balance()

        total_str = f"{total_balance:,.2f} грн".replace(",", " ")

        if total_balance < 0:
            total_text = Text(
                total_str, style="bold red on #2d1315"
            )  # Бордовий фон для ефекту "ВАУ" при боргу
        else:
            total_text = Text(
                f"+{total_str}", style="bold green on #132d15"
            )  # Темно-зелений фон для переплати

        # 2. Створюємо таблицю з увімкненим футером (show_footer=True)
        table = Table(
            title="📊 Стан Особових Рахунків",
            box=ROUNDED,
            border_style="bright_blue",
            header_style="bold cyan on #1a1a2e",
            show_footer=True,
            footer_style="bold",
        )

        # Додаємо колонки та передаємо підписи для нижньої панелі (футера)
        table.add_column("Особовий рахунок", justify="left")
        table.add_column(
            "Постачальник послуг",
            justify="left",
            style="bold white",
            footer=Text("Всього до сплати:", style="bold italic white"),
        )
        table.add_column("ПОТОЧНИЙ БАЛАНС", justify="right", footer=total_text)

        # 3. Заповнюємо таблицю даними
        for item in self.data:
            balance_str = f"{item.balance:,.2f} грн".replace(",", " ")

            if item.balance < 0:
                balance_style = "bold red"
            else:
                balance_style = "bold green"
                balance_str = f"+{balance_str}"

            balance_text = Text(balance_str, style=balance_style)
            table.add_row(
                item.account_number,
                f"{item.provider_details.name} ({item.provider_details.category_details.name})",
                balance_text,
            )

        # Виведення таблиці в консоль
        console.print(table)
