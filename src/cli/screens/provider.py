from typing import Any

from ...api import ProviderCreate
from ..context import AppContext
from .base import Screen
from .builder import builder


def provider_list_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    if not context.current_property:
        input("Помилка контексту - не знайдений поточний об'єкт нерухомості")
        input("Для повернення в головне меню натисніть Enter ...")
        return "main_menu", {}

    providers = context.provider_api.list()
    choices = []
    for provider in providers:
        choices.append(
            {
                "value": {"action": "provider_detail", "params": provider.id},
                "name": f"📁 {provider.name}",
            }
        )
    choices.append(
        {
            "value": {"action": "provider_add"},
            "name": "➕ Створити нового постачальника послуг",
        }
    )
    screen: Screen = (
        builder.add_main_header(context.username)
        .add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}"
        )
        .add_choice_menu(choices, message="Список постачальників послуг:")
        .build(context)
    )
    data = screen.show()
    action = data.get("action")
    if not action:
        raise ValueError("No action")
    params = data.get("params") or {}
    return action, params


def provider_add_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    screen: Screen = (
        builder.add_main_header(context.username)
        .add_menu_header("Меню створення нового постачальника послуг")
        .add_input_component(
            {
                "name": "Назва нового постачальника послуг: ",
            }
        )
        .build(context)
    )
    data = screen.show()
    payload = data.get("payload")
    if not payload:
        raise ValueError("No payload")
    provider_create_dto = ProviderCreate.model_validate(payload)
    context.provider_api.create(provider_create_dto)
    return "provider_list", {}
