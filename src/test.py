from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.styles import Style

# 1. Створюємо кастомні стилі (саме через словник)
custom_style = Style.from_dict(
    {
        "dialog": "bg:#000000",  # Фон вікна
        "dialog.body": "fg:#ffffff",  # Текст вікна
        "red-text": "#ff0000",  # Наш кастомний червоний
        "green-text": "fg:green",  # Наш кастомний зелений
        "bold-text": "bold fg:yellow",  # Наш кастомний жирний жовтий
    }
)

# 2. Формуємо список. Тут name — це список кортежів, який підтримується офіційно!
choices = [
    (
        "colors",  # Що повернеться (value)
        [
            ("class:red-text", "Красный"),
            ("", " и "),
            ("class:green-text", "Зеленый"),
            ("", " текст"),
        ],  # Як відобразиться (name)
    ),
    (
        "important",
        [("class:bold-text", "ВАЖНО:"), ("", " Нажмите сюда для продолжения")],
    ),
    ("normal", "Просто обычный текст"),
]

# 3. Викликаємо діалог вибору
dialog = radiolist_dialog(
    title="Вибір пункту",
    text="Выберите нужный пункт:",
    values=choices,
    style=custom_style,
)

result = dialog.run()
print(f"Вы выбрали: {result}")
