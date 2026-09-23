from ...api import PropertyCreate
from ..context import AppContext
from .builder import builder


def property_detail_screen(context: AppContext):
    property = context.property_api.get(context.current_property.id)
    screen = (
        builder
        .add_main_header(context.username)
        .add_text_label(f"Назва: {property.name}")
        .add_text_label(f"Адреса: {property.address}")
        .add_choice_menu(
            [
                {"value": "meters", "name": "📊 Лічильники"},
                {"value": "bills", "name": "📄 Рахунки на оплату комунальних послуг"},
                {"value": "payments", "name": "💳 Платежі"},
                {"value": "tariffs", "name": "💰 Тарифи"},
                {"value": "benefits", "name": "🛡 Пільги та Субсидії"},
                {"value": "providers", "name": "🔌 Постачальники послуг"},
                {"value": "categories", "name": "🛠 Категорії"},
                {"value": "account_numbers", "name": "🔑 Особові рахунки"},
                {"value": "edit_property", "name": "📝 Редагувати поточний об'єкт нерухомості"},
                {"value": "delete_property", "name": "🗑️ Видалити поточний об'єкт нерухомості"},
            ]
        )
        .build(context)
    )
    data = screen.show()
    return data
