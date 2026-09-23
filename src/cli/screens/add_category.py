from ...api import CategoryCreate
from ..context import AppContext
from .builder import builder


def add_category_screen(context: AppContext):
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
    category_create_dto = CategoryCreate(**data)
    context.category_api.create(category_create_dto)
    return "category_list"
