from typing import Any

from ..context import AppContext
from .base import Screen
from .builder import builder


def meter_list_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    if not context.current_property:
        input("Помилка контексту - не знайдений поточний об'єкт нерухомості")
        input("Для повернення в головне меню натисніть Enter ...")
        return "main_menu", {}

    meters = context.meter_api.list_by_property(property_id=context.current_property.id)

    choices = []
    for meter in meters:
        choices.append(
            {
                "value": {
                    "action": "meter_detail",
                    "params": meter.id,
                },
                "name": f"⏲️ {meter.name}",
            }
        )
    choices.append(
        {
            "value": {"action": "meter_add"},
            "name": "➕ Додати новий лічильник",
        }
    )

    screen: Screen = (
        builder.add_main_header(context.username)
        .add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}"
        )
        .add_choice_menu(choices, message="Список лічильників:")
        .build(context)
    )

    data = screen.show()
    action = data.get("action")
    if not action:
        raise ValueError("No action")
    params = data.get("params") or {}
    return action, params
