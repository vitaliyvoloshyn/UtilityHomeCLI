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
    res = screen.show()
    action = res.get("screen")
    if action is None:
        action = "main_menu"
    params = res.get("params") or {}
    payload = res.get("payload") or {}
    if payload:
        property_create_dto = PropertyCreate.model_validate(payload)
        context.property_api.create(property_create_dto)
    else:
        raise ValueError("Не знайдений payload")
    return action, params


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
                {"value": {"action": "meters"}, "name": "📊 Лічильники"},
                {
                    "value": {"action": "bills"},
                    "name": "📄 Рахунки на оплату комунальних послуг",
                },
                {"value": {"action": "payments"}, "name": "💳 Платежі"},
                {"value": {"action": "tariffs"}, "name": "💰 Тарифи"},
                {"value": {"action": "benefits"}, "name": "🛡 Пільги та Субсидії"},
                {
                    "value": {"action": "provider_list"},
                    "name": "🌐 Постачальники послуг",
                },
                {"value": {"action": "category_list"}, "name": "📁 Категорії"},
                {
                    "value": {"action": "account_number_list"},
                    "name": "🔑 Особові рахунки",
                },
                {
                    "value": {"action": "edit_property"},
                    "name": "📝 Редагувати поточний об'єкт нерухомості",
                },
                {
                    "value": {"action": "delete_property"},
                    "name": "🗑️ Видалити поточний об'єкт нерухомості",
                },
            ]
        )
        .build(context)
    )
    res = screen.show()
    action = res.get("action")
    if action is None:
        raise ValueError("action не знайдено")
    params = res.get("params") or {}
    return action, params
