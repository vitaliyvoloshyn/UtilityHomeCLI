from typing import Any

from ..context import AppContext
from .base import Screen
from .builder import builder


def tariff_list_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    if not context.current_property:
        input("Помилка контексту - не знайдений поточний об'єкт нерухомості")
        input("Для повернення в головне меню натисніть Enter ...")
        return "main_menu", {}

    tariffs = context.tariff_api.list_by_property(
        property_id=context.current_property.id
    )

    tariffs = [tariff for tariff in tariffs if tariff.effective_to is None]

    choices = []
    for tariff in tariffs:
        choices.append(
            {
                "value": {
                    "action": "tariff_detail",
                    "params": tariff.id,
                },
                "name": f"📈 {tariff.name} ({tariff.account_details.provider_details.name}) - {tariff.price_per_unit:.2f}",
            }
        )
    choices.append(
        {
            "value": {"action": "tariff_add"},
            "name": "➕ Додати новий тариф",
        }
    )

    screen: Screen = (
        builder.add_main_header(context.username)
        .add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}"
        )
        .add_choice_menu(choices, message="Список тарифів:")
        .build(context)
    )

    data = screen.show()
    action = data.get("action")
    if not action:
        raise ValueError("No action")
    params = data.get("params") or {}
    return action, params
