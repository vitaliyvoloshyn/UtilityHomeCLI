from typing import Any

from ...api import ProviderAPI, ProviderCreate
from ..context import AppContext
from .builder import builder


def provider_list_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    if not context.current_property:
        input("Помилка контексту - не знайдений поточний об'єкт нерухомості")
        input("Для повернення в головне меню натисніть Enter ...")
        return "main_menu", {}

    providers = context.property_api.list()
    choices = []
    for provider in providers:
        choices.append({"value": provider.id, "name": f"📁 {provider.name}"})
    choices.append({"value": "add_category", "name": "➕ Створити нову категорію"})
    screen = (
        builder.add_main_header(context.username)
        .add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}"
        )
        .add_choice_menu(choices, message="Список категорій:")
        .build(context)
    )
    data = screen.show()
    return data, {}


def add_provider_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    screen = (
        builder.add_main_header(context.username)
        .add_menu_header("Меню створення нової категорії")
        .add_input_component(
            {
                "name": "Назва нової категорії: ",
                "unit_of_measure": "Одиниця вимірювання: ",
            }
        )
        .build(context)
    )
    data = screen.show()
    category_create_dto = ProviderCreate.model_validate(data)
    context.category_api.create(category_create_dto)
    return "category_list", {}
