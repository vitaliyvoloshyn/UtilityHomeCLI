import os
from datetime import date

from loguru import logger

from ..api import *
from ..screen.base_screen import BaseScreen
from ..screen.schema import ComponentDTO
from .builder import *
from .builder.base import BaseBuilder
from .context import AppContext
from .screens import *

# Сюди ж імпортуєте інші екрани, наприклад, DataTableScreen


class Router:
    def __init__(self, context: AppContext):
        self.context = context

        self._builders: dict[str, type[BaseBuilder]] = {
            "login_screen": LoginScreenBuilder,
            "main_menu": MainMenuScreenBuilder,
            "api_error": ErrorScreenBuilder,
            "menu_unauth": UnauthScreenBuilder,
            "register_screen": RegisterScreenBuilder,
            "property_detail": PropertyDetailScreenBuilder,
            "account_list": AccountListScreenBuilder,
            "account_detail": AccountDetailScreenBuilder,
            "category_list": CategoryListScreenBuilder,
            "category_add": CategoryAddScreenBuilder,
            "provider_list": ProviderListScreenBuilder,
            "provider_add": ProviderAddScreenBuilder,
            "tariff_list": TariffListScreenBuilder,
            "tariff_detail": TariffDetailScreenBuilder,
            "tariff_change": TariffChangeScreenBuilder,
            "dev": dev_screen,
            "account_number_add": account_number_add_screen,
            "meter_list": meter_list_screen,
        }
        self.current_builder = "main_menu"

    def get_screen_builder(self, action: str) -> type[BaseBuilder]:
        builder = self._builders.get(action, None)
        if builder is None:
            raise ValueError(f"Помилка: Екран {action} не знайдено.")
        return builder

    def get_screen(self, builder: type[BaseBuilder], **kwargs) -> BaseScreen:
        return builder(self.context, **kwargs).build()

    def run(self):
        dto = ComponentDTO()
        try:
            self.context.connect_to_server()
        except AuthError:
            logger.debug("auth_error")
            self.current_builder = "menu_unauth"
        except APIError as exc:
            print(exc)
            self.context.is_running = False

        while self.context.is_running:
            # Отримуємо об'єкт поточного екрану
            try:
                screen_builder = self.get_screen_builder(self.current_builder)
                logger.debug(screen_builder)
            except ValueError as e:
                print(e)
                break

            screen: BaseScreen = self.get_screen(screen_builder, **dto.params)

            # Рендеримо екран і отримуємо назву наступного
            self.clear_console()
            try:
                dto = screen.show()
                logger.debug(f"dto = {dto}")
                next_screen = dto.action

                match next_screen:
                    case "login":
                        self.login(dto.payload)
                        next_screen = "main_menu"

                    case "register":
                        self.register(dto.payload)
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
                            if property.id == dto.params.get("property_id")
                        )

                    case "category_add_request":
                        self.add_category(dto.payload)
                        next_screen = "category_list"

                    case "provider_add_request":
                        self.add_provider(dto.payload)
                        next_screen = "provider_list"

                    case "tariff_change_request":
                        try:
                            year = dto.payload.get("year")
                            month = dto.payload.get("month")
                            if year is None and month is None:
                                raise ValueError("Не задані рік або місяць")
                            if not isinstance(year, (int, str)) or not isinstance(
                                month, (int, str)
                            ):
                                raise TypeError("Рік/місяць мають бути числом")
                            year = int(year)
                            month = int(month)
                            date_from = self.get_date(year, month)
                            tariff_ch_dto = TariffChange(
                                tariff_id=dto.payload["tariff_id"],
                                new_price=dto.payload["new_price"],
                                effective_from=date_from,
                            )
                            self.context.tariff_api.change_tariff(tariff_ch_dto)
                            next_screen = "tariff_list"
                        except ValueError as e:
                            next_screen = "api_error"
                            self.context.error_message = str(e)

                    case "logout":
                        self.reset_current_property()
                        self.context.logout()
                        next_screen = "menu_unauth"

                    case "exit":
                        self.context.is_running = False
                        break

            except AuthError as e:
                print(e)
                self.input_continue()
                next_screen = "menu_unauth"
            except APIError as exc:
                self.context.error_message = str(exc)
                next_screen = "api_error"
            except KeyboardInterrupt:
                next_screen = "exit"

            self.current_builder = next_screen

    def login(self, payload: dict):
        self.context.login(payload)

    def register(self, payload: dict):
        self.context.api.register(payload)

    def reset_current_property(self):
        self.context.current_property = None

    def clear_console(self):
        # os.system("cls" if os.name == "nt" else "clear")
        ...

    @staticmethod
    def input_continue():
        input("Для продовження натисніть ENTER ...")

    def add_category(self, payload: dict):
        category_dto = CategoryCreate.model_validate(payload)
        self.context.category_api.create(category_dto)

    def add_provider(self, payload: dict):
        provider_dto = ProviderCreate.model_validate(payload)
        self.context.provider_api.create(provider_dto)

    def get_date(self, year: int, month: int):
        return date(year, month, 1)
