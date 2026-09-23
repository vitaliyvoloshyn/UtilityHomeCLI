from ..context import AppContext
from .builder import builder


def main_menu_screen(context: AppContext):
    properties = context.properties
    choices = []
    for property in properties:
        choices.append({"name": f"🏠  {property.name} ({property.address})", "value": property.id})
    choices.append({"name": "Додати новий об'єкт нерухомості", "value": "add_property"})

    screen = (
        builder
        .add_main_header(context.username)
        .add_choice_menu(
            items=choices,
            message="Оберіть об'єкт нерухомості зі списку нижче:",
            include_back_to_main_menu=False
        )
        .build(context)
    )
    res = screen.show()
    if isinstance(res, str):
        return res
    context.current_property = next(filter(lambda prop: prop.id == res, properties))
    return "detail_property"
