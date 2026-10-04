from rich.box import ROUNDED
from rich.console import Console
from rich.table import Table

# Ініціалізація консолі
console = Console()

# Створення таблиці із заокругленими кутами та стильним рамковим оформленням
table = Table(
    title="📊 Стан Особових Рахунків",
    box=ROUNDED,
    border_style="bright_blue",
    header_style="bold cyan on #1a1a2e",
)

# Додавання колонок із заданим вирівнюванням та стилями
table.add_column("ACCOUNT NUMBER", justify="left")
table.add_column("PROVIDER", justify="left", style="bold white")
table.add_column("ПОТОЧНИЙ БАЛАНС", justify="right")

# Тестові дані (додано один позитивний баланс для демонстрації зеленого кольору)
data = [
    ("О/р електро", "Обленерго (Електропостачання)", -10895.04),
    ("0103028-0", "Українське ВКП (Водопостачання)", -2339.78),
    ("0103028-0--98", "Євролінк (Інтернет)", -580.00),
    ("00-проф-", "Профпереробка (Вивіз сміття)", -253.40),
    ("xx-xxx", "Нафтогаз (Газопостачання)", -114.74),
    ("77-yyy", "Тестовий Провайдер (Переплата)", 450.00),  # Приклад позитивного балансу
]

# Заповнення таблиці
for account, provider, balance in data:
    # Форматування виведення валюти
    balance_str = f"{balance:,.2f} грн".replace(",", " ")

    # Динамічний колір залежно від знаку
    if balance < 0:
        balance_style = "bold red"
    else:
        balance_style = "bold green"
        balance_str = f"+{balance_str}"  # Додаємо плюс для краси

    table.add_row(
        account, provider, balance_str, style=balance_style if balance < 0 else None
    )

    # Окремо стилізуємо лише комірку балансу, щоб вся стрічка не ставала червоною/зеленою
    # (Це дозволяє колонці PROVIDER залишатися білою, як в оригіналі)
    table.rows[-1].cells[2].style = balance_style

# Виведення таблиці в консоль
console.print("\n")
console.print(table)
console.print("\n")
