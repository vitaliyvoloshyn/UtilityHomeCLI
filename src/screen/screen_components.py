from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

from InquirerPy.prompts.input import InputPrompt
from InquirerPy.prompts.list import ListPrompt
from pydantic import BaseModel, model_validator
from rich.box import HEAVY, ROUNDED, SQUARE
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..api.models import AccountNumberResponse
from ..api.utility_models import InvoiceResponse

console = Console()


class BaseComponent[T](ABC):
    @abstractmethod
    def render(self) -> T:
        raise NotImplementedError


class MenuHeaderComponent(BaseComponent[dict]):
    def __init__(self, title: str, params: dict | None = None):
        if params is None:
            params = {}
        self.title = title
        self.params = params

    def render(self) -> dict:
        styled_panel = Panel(
            self.title,
            box=ROUNDED,
            border_style="green",
            expand=False,
        )
        console.print(styled_panel)
        return self.params


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


class ChoiceMenu(BaseComponent[dict]):
    def __init__(
        self,
        items: list[dict[str, Any]],
        message: str = "Оберіть дію:",
        add_logout_item: bool = True,
        add_exit_item: bool = True,
        add_back_to_main_menu_item: bool = True,
        add_back_item: bool = True,
    ):
        self.message = message
        self.items = items
        self.add_logout_item = add_logout_item
        self.add_exit_item = add_exit_item
        self.add_back_to_main_menu_item = add_back_to_main_menu_item
        self.add_back_item = add_back_item

    def render(self) -> dict:
        final_choices = self.items
        if self.add_back_item:
            final_choices.append(
                {
                    "name": "↩️ Повернутися у попереднє меню",
                    "value": {"action": "prev_menu"},
                },
            )

        if self.add_back_to_main_menu_item:
            final_choices.append(
                {
                    "name": "🔙 Повернутися у головне меню",
                    "value": {"action": "main_menu"},
                },
            )

        if self.add_logout_item:
            final_choices.append(
                {"name": "🚪 Вийти з акаунту", "value": {"action": "logout"}},
            )

        if self.add_exit_item:
            final_choices.append(
                {"name": "❌ Закрити програму", "value": {"action": "exit"}},
            )

        choice = ListPrompt(
            message=self.message,
            choices=final_choices,
        ).execute()
        return choice


class InputComponent(BaseComponent[dict]):
    def __init__(
        self, messages: dict[str, Any], action: str, is_password: bool = False
    ):
        self.messages = messages
        self.action = action
        self.is_password = is_password

    def render(self) -> dict:
        out_dict = self.messages.copy()
        for key, message in out_dict.items():
            out_dict[key] = InputPrompt(
                message=message, is_password=self.is_password
            ).execute()
        return {"payload": out_dict, "action": self.action}


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


class TableInvoiceList(BaseComponent[None]):
    def __init__(self, data: list[InvoiceResponse]) -> None:
        self.data = data

    def render(self) -> None:
        console.print("\n[bold blue]💵 РАХУНОК ЗА КОМУНАЛЬНІ ПОСЛУГИ[/bold blue]\n")
        for invoice in self.data:
            # --- БЛОК 1: ЗАГАЛЬНА ІНФОРМАЦІЯ (БЕЗ РАМОК) ---

            # Використовуємо box=None, щоб повністю сховати сітку
            info_table = Table(show_header=False, box=None, padding=(0, 1, 0, 1))

            # Задаємо 4 колонки для вирівнювання лівої та правої частин
            info_table.add_column(width=22, style="bold cyan")  # Назва поля (ліворуч)
            info_table.add_column(width=35)  # Значення поля (ліворуч)
            info_table.add_column(
                width=20, justify="right", style="bold cyan"
            )  # Назва поля (праворуч)
            info_table.add_column(width=18, justify="right")  # Значення поля (праворуч)

            # Додаємо рядки загальної інформації
            info_table.add_row(
                "Постачальник послуг:",
                invoice.provider_name,
                "Розрахунковий період:",
                invoice.billing_period_display,
            )
            info_table.add_row("О/р:", f"[yellow]{invoice.account_number}[/]", "", "")
            info_table.add_row(
                "Пільги:",
                f"[magenta]{invoice.benefit_name}[/]",
                "Статус:",
                self.get_status_text(invoice.status_display),
            )

            # --- БЛОК 2: ТАБЛИЦЯ НАРАХУВАНЬ (З РАМКАМИ) ---
            # Використовуємо коробковий стиль SQUARE та вмикаємо лінії між рядками
            calc_table = Table(
                show_header=True, box=SQUARE, show_lines=True, border_style="gray37"
            )

            calc_table.add_column(
                "Послуга / Тариф", width=25, header_style="bold white on blue"
            )
            calc_table.add_column(
                "Тариф", width=12, justify="right", header_style="bold white on blue"
            )
            calc_table.add_column(
                "Попередні показники",
                width=12,
                justify="right",
                header_style="bold white on blue",
            )
            calc_table.add_column(
                "Поточні показники",
                width=12,
                justify="right",
                header_style="bold white on blue",
            )
            calc_table.add_column(
                "Спожито", width=12, justify="right", header_style="bold white on blue"
            )
            calc_table.add_column(
                "Пільги", width=12, justify="right", header_style="bold white on blue"
            )
            calc_table.add_column(
                "Нараховано",
                width=15,
                justify="right",
                header_style="bold white on blue",
            )

            for item in invoice.items:
                # Дані розрахунків
                calc_table.add_row(
                    item.tariff_name,
                    str(item.tariff_price_at_billing),
                    str(item.previous_reading),
                    str(item.current_reading),
                    str(item.consumption),
                    str(item.benefit_discount),
                    str(item.base_amount),
                )

                # Фінальний підсумок (використовуємо порожні комірки для зміщення тексту праворуч)
            calc_table.add_row(
                "",
                "",
                "",
                "",
                "",
                "[bold white on dark_green] Всього до сплати [/]",
                f"[bold white on yellow] {invoice.amount_due} [/]",
            )

            # --- ВИВЕДЕННЯ В КОНСОЛЬ ---

            console.print(info_table)
            console.print("\n")  # Невеликий відступ між блоками
            console.print(calc_table)

    # Функція для підсвічування статусу
    @staticmethod
    def get_status_text(status_value: str) -> Text:
        status_lower = status_value.lower()
        if "неоплачено" in status_lower:
            return Text(
                f" {status_value} ", style="bold white on red"
            )  # Червона плашка
        elif "частково оплачено" in status_lower:
            return Text(
                f" {status_value} ", style="bold black on yellow"
            )  # Жовта плашка
        return Text(status_value, style="bold green")


class TariffDetailDTO(BaseModel):
    """
    headers - Заголовки таблиці
    rows - рядки таблиці
    Колонки таблиці вносяться в такій послідовності: Назва тарифу, значення тарифу, тип тарифу, дата початку дії, лічильник, оператор
    """

    headers: Sequence[str]
    row: Sequence[str]

    @model_validator(mode="after")
    def validate_rows_length_matches_headers(self) -> "TariffDetailDTO":

        # Перевіряємо кожну стрічку на відповідність довжині headers

        if len(self.headers) != len(self.row):
            raise ValueError(
                f"Невідповідність розміру: рядок з даними має довжину {len(self.row)}, "
                f"але очікувалось {len(self.headers)} (відповідно до кількості headers)."
            )
        return self


class TableTariffDetail(BaseComponent[None]):
    def __init__(self, data: TariffDetailDTO) -> None:
        self.data = data

    def render(self) -> None:
        console.print("\n[bold blue]💵 РАХУНОК ЗА КОМУНАЛЬНІ ПОСЛУГИ[/bold blue]\n")

        # --- БЛОК 2: ТАБЛИЦЯ НАРАХУВАНЬ (З РАМКАМИ) ---
        # Використовуємо коробковий стиль SQUARE та вмикаємо лінії між рядками
        row_params_1 = {
            "width": 25,
            "header_style": "bold white on blue",
        }
        row_params = {
            "width": 12,
            "justify": "right",
            "header_style": "bold white on blue",
        }
        calc_table = Table(
            show_header=True, box=SQUARE, show_lines=True, border_style="gray37"
        )
        # (calc_table.add_column(h, **row_params) for h in self.data.headers)
        for index, header in enumerate(self.data.headers):
            if index == 0:
                calc_table.add_column(header, **row_params_1)
            else:
                calc_table.add_column(header, **row_params)

        calc_table.add_row(*self.data.row)
        # (calc_table.add_row(r) for r in self.data.row)

        # --- ВИВЕДЕННЯ В КОНСОЛЬ ---

        console.print(calc_table)
