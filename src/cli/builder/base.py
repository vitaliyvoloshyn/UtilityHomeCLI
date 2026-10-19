from copy import deepcopy
from typing import Any

from ...api import *
from ...screen.base_screen import BaseScreen
from ...screen.screen_components import (
    AppHeader,
    ChoiceMenu,
    InputComponent,
    MenuHeaderComponent,
    TableAccountsList,
    TableInvoiceList,
    TableTariffDetail,
    TariffDetailDTO,
    TextLabel,
)
from ..context import AppContext


class BaseBuilder:
    def __init__(self, context: AppContext, **kwargs):
        self.screen: BaseScreen = BaseScreen(context)
        self.context = context
        self.base_screen()

    def reset(self) -> BaseScreen:
        self.screen = BaseScreen(self.context)
        return self.screen

    def add_main_header(self, username: str):
        self.screen.add(AppHeader(username))
        return self

    def add_menu_header(self, title: str, params: dict | None = None):
        self.screen.add(MenuHeaderComponent(title, params))
        return self

    def add_choice_menu(
        self,
        items: list[dict[str, Any]],
        message: str = "Оберіть дію:",
        add_back_item: bool = True,
        add_back_to_main_menu_item: bool = True,
        add_logout_item: bool = True,
        add_exit_item: bool = True,
    ):
        """Приймає список типу
        [
            {"name": "Зареєструватися", "value": {"...":"registr"}},
            {"name": "Авторизуватися", "value": {"...":"login"}},
        ]
        """
        self.screen.add(
            ChoiceMenu(
                items=items,
                message=message,
                add_back_item=add_back_item,
                add_back_to_main_menu_item=add_back_to_main_menu_item,
                add_logout_item=add_logout_item,
                add_exit_item=add_exit_item,
            )
        )
        return self

    def add_input_component(
        self, messages: dict[str, str], action: str, is_password: bool = False
    ):
        """Приймає словник та повертає цей же словник, але замість значень підставляє значення, які ввів юзер.
        Value вхідного словника це меседжі, які будуть показані юзеру для введення даних"""
        self.screen.add(InputComponent(messages, action, is_password))
        return self

    def add_text_label(self, text: str):
        self.screen.add(TextLabel(text))
        return self

    def add_table_account_list(self, data: list[AccountNumberResponse]):
        self.screen.add(TableAccountsList(data))
        return self

    def add_table_invoice_list(self, data: list[InvoiceResponse]):
        self.screen.add(TableInvoiceList(data))
        return self

    def add_table_tariff_detail(self, data: TariffDetailDTO):
        self.screen.add(TableTariffDetail(data))
        return self

    def base_screen(self):
        self.add_main_header(self.context.username)

    def build(self) -> BaseScreen:
        screen_copy = deepcopy(self.screen)

        self.reset()
        return screen_copy

    def get_categories(self) -> list[CategoryResponse]:
        assert self.context.current_property is not None
        return self.context.category_api.list(
            property_id=self.context.current_property.id
        )

    def get_providers(self) -> list[ProviderResponse]:
        assert self.context.current_property is not None
        return self.context.provider_api.list(
            property_id=self.context.current_property.id
        )

    def get_provider_choices(self) -> list:
        choices = []
        providers = self.get_providers()
        for provider in providers:
            choices.append(
                {
                    "value": {
                        "action": "provider_detail",
                        "params": {"provider_id": provider.id},
                    },
                    "name": f"📁 {provider.name}",
                }
            )
        choices.append(
            {
                "value": {"action": "provider_add"},
                "name": "➕ Додати нового постачальника послуг",
            }
        )
        return choices

    def get_category_choices(self) -> list:
        choices = []
        categories = self.get_categories()
        for category in categories:
            choices.append(
                {
                    "value": {
                        "action": "category_detail",
                        "params": {"category_id": category.id},
                    },
                    "name": f"📁 {category.name}",
                }
            )
        choices.append(
            {
                "value": {"action": "category_add"},
                "name": "➕ Створити нову категорію",
            }
        )
        return choices


class UnauthScreenBuilder(BaseBuilder):
    def __init__(self, context: AppContext, **kwargs):
        super().__init__(context)
        self.add_menu_header("Стартове меню")
        self.add_choice_menu(
            [
                {"name": "🔑 Авторизуватися", "value": {"action": "login_screen"}},
                {"name": "📝 Зареєструватися", "value": {"action": "register_screen"}},
            ],
            add_back_item=False,
            add_back_to_main_menu_item=False,
            add_logout_item=False,
        )

    def base_screen(self):
        self.add_main_header("Не авторизований користувач")


class MainMenuScreenBuilder(BaseBuilder):
    def __init__(self, context: AppContext, **kwargs):
        super().__init__(context)
        self.add_menu_header("Головне меню")
        self.add_choice_menu(
            items=self.get_choices(),
            message="Оберіть об'єкт нерухомості зі списку нижче:",
            add_back_to_main_menu_item=False,
        )

    def get_choices(self) -> list:

        choices: list = []
        properties = self.context.properties

        for property in properties:
            choices.append(
                {
                    "name": f"🏠  {property.name} ({property.address})",
                    "value": {
                        "action": "property_detail",
                        "params": {"property_id": property.id},
                    },
                }
            )

        choices.append(
            {
                "name": "➕ Додати новий об'єкт нерухомості",
                "value": {"action": "property_add"},
            }
        )

        return choices


class ErrorScreenBuilder(BaseBuilder):
    def __init__(self, context: AppContext, **kwargs):
        super().__init__(context)
        self.add_main_header(context.username or "Не авторизований користувач")
        self.add_text_label(context.error_message)
        self.add_choice_menu([])


class LoginScreenBuilder(BaseBuilder):
    def __init__(self, context: AppContext, **kwargs):
        super().__init__(context)
        self.add_input_component(
            {"username": "Введіть email: "},
            "login",
        )
        self.add_input_component(
            {"password": "Введіть пароль: "},
            "login",
            is_password=True,
        )


class RegisterScreenBuilder(BaseBuilder):
    def __init__(self, context: AppContext, **kwargs):
        super().__init__(context)
        self.add_menu_header("Меню реєстрації нового користувача")
        self.add_input_component(
            {
                "first_name": "Ваше ім'я: ",
                "last_name": "Ваше прізвище: ",
                "email": "Введіть email: ",
            },
            "register",
        )
        self.add_input_component(
            {
                "password": "Введіть пароль: ",
            },
            "register",
            is_password=True,
        )


class PropertyDetailScreenBuilder(BaseBuilder):
    def __init__(self, context: AppContext, **kwargs):
        super().__init__(context)
        assert context.current_property is not None
        self.add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}"
        )
        self.add_choice_menu(
            [
                {
                    "value": {"action": "account_list"},
                    "name": "🔑 Особові рахунки",
                },
                {"value": {"action": "meter_list"}, "name": "⏲️ Лічильники"},
                {
                    "value": {"action": "bill_list"},
                    "name": "📄 Рахунки на оплату комунальних послуг",
                },
                {"value": {"action": "payment_list"}, "name": "💳 Платежі"},
                {"value": {"action": "tariff_list"}, "name": "📈 Тарифи"},
                {"value": {"action": "benefit_list"}, "name": "🛡 Пільги та Субсидії"},
                {
                    "value": {"action": "provider_list"},
                    "name": "🌐 Постачальники послуг",
                },
                {"value": {"action": "category_list"}, "name": "📁 Категорії"},
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


class AccountListScreenBuilder(BaseBuilder):
    def __init__(self, context: AppContext, **kwargs):
        super().__init__(context)
        assert context.current_property is not None
        self.accounts = self.get_accounts(context.current_property.id)
        self.add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}"
        )
        self.add_table_account_list(self.accounts)
        self.add_choice_menu(self.get_choices(), message="Список особових рахунків:")

    def get_accounts(self, property_id: int) -> list[AccountNumberResponse]:
        account_numbers = self.context.account_number_api.list(property_id=property_id)

        return account_numbers

    def get_choices(self) -> list:
        choices = []
        for account in self.accounts:
            choices.append(
                {
                    "value": {
                        "action": "account_detail",
                        "params": {"account_id": account.id},
                    },
                    "name": f"📁 {account.account_number} - {account.provider_details.name}",
                }
            )
        choices.append(
            {
                "value": {"action": "account_number_add"},
                "name": "➕ Створити новий особовий рахунок",
            }
        )

        return choices


class AccountDetailScreenBuilder(BaseBuilder):
    def __init__(self, context: AppContext, **kwargs):
        super().__init__(context)
        assert context.current_property is not None
        self.add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}"
        )
        self.add_table_invoice_list(self.get_invoices(kwargs["account_id"]))
        self.add_choice_menu([], message="Список особових рахунків:")

    def get_invoices(self, account_id: int):
        return self.context.invoice_api.list(
            account_id=account_id,
            status=["unpaid", "partially_paid"],
        )


class CategoryListScreenBuilder(BaseBuilder):
    def __init__(self, context: AppContext, **kwargs):
        super().__init__(context)
        assert context.current_property is not None
        self.add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}"
        )
        self.add_choice_menu(
            self.get_category_choices(),
            message="Список категорій послуг:",
        )


class CategoryAddScreenBuilder(BaseBuilder):
    def __init__(self, context: AppContext, **kwargs):
        super().__init__(context)
        assert context.current_property is not None
        self.add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}"
        )
        self.add_input_component(
            {"name": "Введіть назву нової категорії:"}, "category_add_request"
        )


class ProviderListScreenBuilder(BaseBuilder):
    def __init__(self, context: AppContext, **kwargs):
        super().__init__(context)
        assert context.current_property is not None
        self.add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}"
        )
        self.add_choice_menu(
            self.get_provider_choices(),
            message="Список постачальників послуг:",
        )


class ProviderAddScreenBuilder(BaseBuilder):
    def __init__(self, context: AppContext, **kwargs):
        super().__init__(context)
        assert context.current_property is not None
        categories = self.get_categories()
        choices = []
        for category in categories:
            choices.append(
                {
                    "value": {
                        "action": "provider_add_request",
                        "payload": {"category": category.id},
                    },
                    "name": f"📁 {category.name}",
                }
            )
        self.add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}"
        )
        self.add_input_component(
            {"name": "Введіть назву нового постачальника послуг:"},
            "provider_add_request",
        )
        self.add_choice_menu(choices)


class TariffListScreenBuilder(BaseBuilder):
    def __init__(self, context: AppContext, **kwargs):
        super().__init__(context)
        assert context.current_property is not None
        self.add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}"
        )
        self.add_choice_menu(
            self.get_tariffs_choices(self.get_tariffs()),
            message="Список тарифів:",
        )

    def get_tariffs(self) -> list[TariffResponse]:
        assert self.context.current_property is not None
        tariffs = self.context.tariff_api.list(
            property_id=self.context.current_property.id
        )
        return [tariff for tariff in tariffs if tariff.is_active]

    def get_tariffs_choices(self, tariffs: list[TariffResponse]) -> list:
        choices = []
        for tariff in tariffs:
            choices.append(
                {
                    "value": {
                        "action": "tariff_detail",
                        "params": {"tariff_id": tariff.id},
                    },
                    "name": f"📁 {tariff.account_details.provider_details.name} - {tariff.name}",
                }
            )
        choices.append(
            {
                "value": {"action": "tariff_add"},
                "name": "➕ Створити нову категорію",
            }
        )
        return choices


class TariffDetailScreenBuilder(BaseBuilder):
    def __init__(self, context: AppContext, **kwargs):
        super().__init__(context)
        tariff_id = kwargs.get("tariff_id")
        assert tariff_id is not None
        assert context.current_property is not None
        self.tariff = self.get_current_teariff(tariff_id)
        self.add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}"
        )
        self.add_menu_header(
            f"Деталізація по тарифу: {self.tariff.name} ({self.tariff.price_per_unit:.2f})"
        )
        self.add_table_tariff_detail(self.get_tariff_dto(self.tariff))
        self.add_choice_menu(
            [
                {
                    "name": "🆙 Зміна поточного тарифу",
                    "value": {
                        "action": "tariff_change",
                        "params": {"tariff_id": self.tariff.id},
                    },
                }
            ]
        )

    def get_current_teariff(self, tariff_id: int) -> TariffResponse:
        cur_tariff = self.context.tariff_api.get(tariff_id)
        return cur_tariff

    def get_tariff_dto(self, cur_tariff: TariffResponse) -> TariffDetailDTO:
        headers = (
            "Назва",
            "Значення",
            "Тип",
            "Дата початку дії",
            "Лічильник",
            "Оператор",
        )
        meter = cur_tariff.meter_details.name if cur_tariff.meter_details else "-"
        row = (
            cur_tariff.name,
            str(f"{cur_tariff.price_per_unit:.2f}"),
            cur_tariff.charge_type_display,
            str(cur_tariff.effective_from),
            meter,
            cur_tariff.account_details.provider_details.name,
        )
        return TariffDetailDTO(headers=headers, row=row)


class TariffChangeScreenBuilder(BaseBuilder):
    """Зміна тарифу (коли оператор змінив тариф)"""

    def __init__(self, context: AppContext, **kwargs):
        super().__init__(context)
        tariff_id = kwargs.get("tariff_id")
        assert tariff_id is not None
        assert context.current_property is not None
        self.add_menu_header(
            f"{context.current_property.name}, {context.current_property.address}",
            params={"payload": {"tariff_id": tariff_id}},
        )
        self.add_input_component(
            messages={
                "new_price": "Введіть нове значення тарифу: ",
                "month": "Введіть місяць, з якого починає діяти новий тариф (число від 1 до 12): ",
                "year": "Введіть рік, з якого починає діяти новий тариф (напр, 2026): ",
            },
            action="tariff_change_request",
        )
