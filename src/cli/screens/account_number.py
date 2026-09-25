from os import name
from typing import Any

from loguru import logger

from ...api import AccountNumberCreate
from ..context import AppContext
from .base import Screen
from .builder import builder


def account_number_list_screen(
    context: AppContext, **kwargs
) -> tuple[str, dict[str, Any]]:
    if not context.current_property:
        input("Помилка контексту - не знайдений поточний об'єкт нерухомості")
        input("Для повернення в головне меню натисніть Enter ...")
        return "main_menu", {}

    account_numbers = context.account_number_api.list()
    choices = []
    for account_number in account_numbers:
        choices.append(
            {
                "value": {
                    "action": "account_number_detail",
                    "params": account_number.id,
                },
                "name": f"📁 {account_number.account_number} - {account_number.provider_details.name}",
            }
        )
    choices.append(
        {
            "value": {"action": "account_number_add"},
            "name": "➕ Створити новий особовий рахунок",
        }
    )
    screen: Screen = (
        builder.add_main_header(context.username)
        .add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}"
        )
        .add_choice_menu(choices, message="Список особових рахунків:")
        .build(context)
    )
    data = screen.show()
    action = data.get("action")
    if not action:
        raise ValueError("No action")
    params = data.get("params") or {}
    return action, params


def account_number_add_screen(
    context: AppContext, **kwargs
) -> tuple[str, dict[str, Any]]:
    if not context.current_property:
        input("Помилка контексту - не знайдений поточний об'єкт нерухомості")
        input("Для повернення в головне меню натисніть Enter ...")
        return "main_menu", {}

    providers = context.provider_api.list()

    providers_choices = []
    for provider in providers:
        providers_choices.append(
            {
                "name": provider.name,
                "value": {"action": "account_number_list", "params": provider.id},
            }
        )

    screen: Screen = (
        builder.add_main_header(context.username)
        .add_menu_header("Меню створення нового особового рахунка")
        .add_input_component(
            {
                "account_number": "Номер особового рахунка: ",
            }
        )
        .add_choice_menu(
            providers_choices,
            message="Оберіть провайдера, до якого буде прив'язаний цей особовий рахунок:",
        )
        .build(context)
    )

    data = screen.show()
    action = data["action"]
    if not action:
        raise ValueError("No action")
    params = data.get("params") or None
    if not params:
        raise ValueError("No params")
    payload = data.get("payload") or None
    if not payload:
        raise ValueError("No payload")
    payload["provider"] = params
    payload["property"] = context.current_property.id
    account_number_create_dto = AccountNumberCreate.model_validate(payload)
    context.account_number_api.create(account_number_create_dto)
    return action, {}
