from ...api import PropertyCreate
from ..context import AppContext
from .builder import builder


def add_property_screen(context: AppContext):
    screen = (
        builder
        .add_main_header(context.username)
        .add_input_component(
            {"name": "Назва об'єкта нерухомості: ", "address": "Адреса об'єкта нерухомості: "}
        )
        .build(context)
    )
    data = screen.show()
    property_create_dto = PropertyCreate(**data)
    context.property_api.create(property_create_dto)
    return "main_menu"
