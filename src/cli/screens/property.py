from typing import Any

from ...api import PropertyCreate
from ..context import AppContext
from .builder import builder


def add_property_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    screen = (
        builder.add_main_header(context.username)
        .add_menu_header("Меню створення нового об'єкта нерухомості")
        .add_input_component(
            {
                "name": "Назва об'єкта нерухомості: ",
                "address": "Адреса об'єкта нерухомості: ",
            }
        )
        .build(context)
    )
    data = screen.show()
    property_create_dto = PropertyCreate.model_validate(data)
    context.property_api.create(property_create_dto)
    return "main_menu", {}


def property_detail_screen(context: AppContext, **kwargs) -> tuple[str, dict[str, Any]]:
    if not context.current_property:
        input("Помилка контексту - не знайдений поточний об'єкт нерухомості")
        input("Для повернення в головне меню натисніть Enter ...")
        return "main_menu", {}

    screen = (
        builder.add_main_header(context.username)
        .add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}"
        )
        .add_choice_menu(
            [
                {"value": "meters", "name": "📊 Лічильники"},
                {"value": "bills", "name": "📄 Рахунки на оплату комунальних послуг"},
                {"value": "payments", "name": "💳 Платежі"},
                {"value": "tariffs", "name": "💰 Тарифи"},
                {"value": "benefits", "name": "🛡 Пільги та Субсидії"},
                {"value": "providers", "name": "🌐 Постачальники послуг"},
                {"value": "category_list", "name": "📁 Категорії"},
                {"value": "account_numbers", "name": "🔑 Особові рахунки"},
                {
                    "value": "edit_property",
                    "name": "📝 Редагувати поточний об'єкт нерухомості",
                },
                {
                    "value": "delete_property",
                    "name": "🗑️ Видалити поточний об'єкт нерухомості",
                },
            ]
        )
        .build(context)
    )
    data = screen.show()
    return data, {}
