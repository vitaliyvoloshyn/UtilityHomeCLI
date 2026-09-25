from typing import Any

from ..context import AppContext
from .builder import builder


def main_menu_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    properties = context.properties
    choices = []
    for property in properties:
        choices.append(
            {
                "name": f"🏠  {property.name} ({property.address})",
                "value": {"action": "detail_property", "params": f"{property.id}"},
            }
        )
    choices.append(
        {
            "name": "➕ Додати новий об'єкт нерухомості",
            "value": {"action": "add_property"},
        }
    )

    screen = (
        builder.add_main_header(context.username)
        .add_menu_header("Головне меню")
        .add_choice_menu(
            items=choices,
            message="Оберіть об'єкт нерухомості зі списку нижче:",
            include_back_to_main_menu=False,
        )
        .build(context)
    )
    res = screen.show()
    action = res.get("action")
    if not action:
        raise ValueError("Не вдалося отримати об'єкт action")
    property_id = res.get("params")
    if property_id:
        context.current_property = next(
            filter(lambda prop: prop.id == int(property_id), properties)
        )
    return action, {}
