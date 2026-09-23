from ..context import AppContext
from .builder import builder


def category_list_screen(context: AppContext):
    categories = context.category_api.list()
    choices = []
    for category in categories:
        choices.append({"value": category.id, "name": f"📁 {category.name}"})
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
    return data
