from typing import Any

from ...api import CategoryCreate
from ..context import AppContext
from .builder import builder


def category_list_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    if not context.current_property:
        input("Помилка контексту - не знайдений поточний об'єкт нерухомості")
        input("Для повернення в головне меню натисніть Enter ...")
        return "main_menu", {}

    categories = context.category_api.list()
    choices = []
    for category in categories:
        choices.append(
            {
                "value": {"action": "category_detail", "params": category.id},
                "name": f"📁 {category.name}",
            }
        )
    choices.append(
        {"value": {"action": "add_category"}, "name": "➕ Створити нову категорію"}
    )
    screen = (
        builder.add_main_header(context.username)
        .add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}"
        )
        .add_choice_menu(choices, message="Список категорій:")
        .build(context)
    )
    data = screen.show()
    action = data.get("action")
    if not action:
        raise ValueError("No action")
    params = data.get("params") or {}
    return action, params


def add_category_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    screen = (
        builder.add_main_header(context.username)
        .add_menu_header("Меню створення нової категорії")
        .add_input_component(
            {
                "name": "Назва нової категорії: ",
            }
        )
        .build(context)
    )
    data = screen.show()
    payload = data.get("payload")
    if not payload:
        raise ValueError("No payload")
    category_create_dto = CategoryCreate.model_validate(payload)
    context.category_api.create(category_create_dto)
    return "category_list", {}
