import os
from datetime import date

from loguru import logger

from ..api import *
from ..screen.base_screen import BaseScreen
from ..screen.schema import ComponentDTO
from .builder import *
from .builder.base import (
    BaseBuilder,
    InputReadingValueScreenBuilder,
    PaymentSuccessScreenBuilder,
)
from .context import AppContext


class ScreenHistory:
    skipped_actions = (
        "",
        "back_step",
        "menu_unauth",
        "generate_bills",
        "payment",
        "payment_success",
        "recalculate",
        "recalculate_success",
        "input_readings_value",
        "invoice_detail",
    )

    def __init__(self):
        logger.debug("Init class ScreenHistory")
        self._screen_history: list[ComponentDTO] = []

    def save(self, screen: ComponentDTO):
        if screen.action in self.skipped_actions:
            return
        if not isinstance(screen, ComponentDTO):
            raise TypeError("Аргумент screen не являється об'єктом класу ComponentDTO")
        if len(self._screen_history) > 0:  # noqa: SIM102
            if self._screen_history[-1].action == screen.action:
                return
        self._screen_history.append(screen)

    def get(self) -> ComponentDTO:
        if len(self._screen_history) == 0:
            raise ValueError("Історія наразі не містить ніяких записів")
        screen = self._screen_history.pop()
        return screen


def get_date(year: int, month: int):
    return date(year, month, 1)


class Router:
    def __init__(self, context: AppContext):
        self.context = context
        self.history = ScreenHistory()

        self._builders: dict[str, type[BaseBuilder]] = {
            "login_screen": LoginScreenBuilder,
            "main_menu": MainMenuScreenBuilder,
            "api_error": ErrorScreenBuilder,
            "menu_unauth": UnauthScreenBuilder,
            "register_screen": RegisterScreenBuilder,
            "property_detail": PropertyDetailScreenBuilder,
            "account_list": AccountListScreenBuilder,
            "invoice_detail": InvoiceDetailScreenBuilder,
            "account_add": AccountAddScreenBuilder,
            "category_list": CategoryListScreenBuilder,
            "category_add": CategoryAddScreenBuilder,
            "provider_list": ProviderListScreenBuilder,
            "provider_add": ProviderAddScreenBuilder,
            "tariff_list": TariffListScreenBuilder,
            "tariff_detail": TariffDetailScreenBuilder,
            "tariff_change": TariffChangeScreenBuilder,
            "tariff_add": TariffAddScreenBuilder,
            "meter_readings_input": MeterReadingsInputScreenBuilder,
            "input_readings_value": InputReadingValueScreenBuilder,
            "consumption_meter_list": ConsumptionMeterListScreenBuilder,
            "readings_list": ConsumptionListScreenBuilder,
            "generate_bills_success": GenerateBillsSuccessScreenBuilder,
            "regenerate_bill_success": InvoiceRegenerateSuccessScreenBuilder,
            "payment": PaymentScreenBuilder,
            "payment_success": PaymentSuccessScreenBuilder,
            "recalculate": RecalculateScreenBuilder,
            "recalculate_success": RecalculateSuccessScreenBuilder,
            "invoice_list": InvoiceListScreenBuilder,
            "payment_account_list": PaymentAccountListScreenBuilder,
            "payment_list": PaymentListScreenBuilder,
        }

    def get_screen_builder(self, action: str) -> type[BaseBuilder]:
        builder = self._builders.get(action, None)
        if builder is None:
            raise ValueError(f"Помилка: Екран {action} не знайдено.")
        return builder

    def get_screen(self, builder: type[BaseBuilder], dto) -> BaseScreen:
        return builder(self.context, dto).build()

    def run(self):
        initial_dto = ComponentDTO(action="main_menu")
        cur_dto = ComponentDTO(action="main_menu")
        prev_dto = cur_dto
        try:
            self.context.connect_to_server()
        except AuthError:
            logger.debug("auth_error")
            cur_dto = ComponentDTO(action="menu_unauth")
        except APIError as exc:
            print(exc)
            self.context.is_running = False

        while self.context.is_running:
            # Отримуємо об'єкт поточного екрану
            try:
                screen_builder = self.get_screen_builder(cur_dto.action)
            except ValueError as e:
                print(e)
                break

            screen: BaseScreen = self.get_screen(screen_builder, cur_dto)

            # Рендеримо екран і отримуємо назву наступного
            self.clear_console()
            try:
                cur_dto = screen.show()
                logger.debug(f"dto = {cur_dto}")
                next_screen = cur_dto.action

                match next_screen:
                    case "login":
                        self.context.login(cur_dto.payload)
                        cur_dto.action = "main_menu"

                    case "register":
                        self.register(cur_dto.payload)
                        print(
                            "Пройдіть верифікацію за посиланням у повідомленні у Вашій поштовій скриньці.\nПотім Ви зможете авторизуватися"
                        )
                        self.input_continue()

                    case "main_menu":
                        self.reset_current_property()

                    case "property_detail":
                        self.context.current_property = next(
                            property
                            for property in self.context.properties
                            if property.id == cur_dto.params.get("property_id")
                        )

                    case "category_add_request":
                        self.add_category(cur_dto.payload)
                        cur_dto.action = "category_list"

                    case "provider_add_request":
                        self.add_provider(cur_dto.payload)
                        cur_dto.action = "provider_list"

                    case "tariff_change_request":
                        try:
                            year = cur_dto.payload.get("year")
                            month = cur_dto.payload.get("month")
                            if year is None and month is None:
                                raise ValueError("Не задані рік або місяць")
                            if not isinstance(year, (int, str)) or not isinstance(
                                    month, (int, str)
                            ):
                                raise TypeError("Рік/місяць мають бути числом")
                            year = int(year)
                            month = int(month)
                            date_from = get_date(year, month)
                            tariff_ch_dto = TariffChange(
                                tariff_id=cur_dto.payload["tariff_id"],
                                new_price=cur_dto.payload["new_price"],
                                effective_from=date_from,
                            )
                            self.context.tariff_api.change_tariff(tariff_ch_dto)
                            cur_dto.action = "tariff_list"
                        except ValueError as e:
                            cur_dto.action = "api_error"
                            self.context.error_message = str(e)

                    case "add_readings_request":
                        data = MeterReadingCreate(
                            meter=cur_dto.payload.get("meter_id"),  # type: ignore
                            reading_value=cur_dto.payload.get("reading_value"),  # type: ignore
                            reading_date=date.today(),
                        )
                        self.context.meter_readings_api.create(data)
                        cur_dto.action = "meter_readings_input"

                    case "tariff_add_request":
                        self.context.tariff_api.create(
                            TariffCreate.model_validate(cur_dto.payload)
                        )
                        cur_dto.action = "tariff_list"

                    case "account_add_request":
                        cur_dto.payload["property"] = self.context.current_property.id  # type: ignore
                        self.context.account_number_api.create(
                            AccountNumberCreate.model_validate(cur_dto.payload)
                        )
                        cur_dto.action = "account_list"

                    case "generate_bills":
                        self.context.invoice_api.generate_bills()
                        cur_dto.action = "generate_bills_success"

                    case "payment_request":
                        cur_dto.params.update(cur_dto.payload)
                        self.context.account_number_api.top_up(
                            amount=cur_dto.payload.get("amount"),  # type: ignore
                            account_id=cur_dto.params.get("account_id"),  # type: ignore
                        )
                        cur_dto.action = "payment_success"

                    case "recalculate_request":
                        data = AccountNumberRecalculate.model_validate(cur_dto.payload)
                        self.context.account_number_api.recalculate(data)
                        cur_dto.action = "recalculate_success"

                    case "regenerate_request":
                        invoice_id = cur_dto.params.get("invoice_id")
                        if invoice_id:
                            self.context.invoice_api.regenerate_bill(invoice_id)
                            cur_dto.action = "regenerate_bill_success"
                        else:
                            cur_dto.action = "api_error"

                    case "back_step":
                        try:
                            cur_dto = self.history.get()
                        except ValueError:
                            cur_dto = initial_dto
                        cur_dto.action = cur_dto.action
                        prev_dto = ComponentDTO()

                    case "logout":
                        self.reset_current_property()
                        self.context.logout()
                        cur_dto.action = "menu_unauth"

                    case "exit":
                        self.context.is_running = False
                        break

            except AuthError as e:
                print(e)
                self.input_continue()
                cur_dto.action = "menu_unauth"
            except APIError as exc:
                self.context.error_message = str(exc)
                cur_dto.action = "api_error"
            except KeyboardInterrupt:
                cur_dto.action = "exit"

            # self.current_builder = next_screen
            self.history.save(prev_dto)
            logger.debug(self.history._screen_history)
            prev_dto = cur_dto

    def login(self, payload: dict):
        self.context.login(payload)

    def register(self, payload: dict):
        self.context.api.register(payload)

    def reset_current_property(self):
        self.context.current_property = None

    @staticmethod
    def clear_console():
        # ...
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def input_continue():
        input("Для продовження натисніть ENTER ...")

    def add_category(self, payload: dict):
        category_dto = CategoryCreate.model_validate(payload)
        self.context.category_api.create(category_dto)

    def add_provider(self, payload: dict):
        provider_dto = ProviderCreate.model_validate(payload)
        self.context.provider_api.create(provider_dto)
