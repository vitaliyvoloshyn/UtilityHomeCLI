from types import NoneType

from ..api import (
    AccountNumberAPI,
    APIClient,
    CategoryAPI,
    InvoiceAPI,
    MeterAPI,
    MeterReadingAPI,
    PropertyAPI,
    PropertyResponse,
    ProviderAPI,
    TariffAPI,
)
from ..api.session import session


class AppContext:
    def __init__(
        self,
        api: type[APIClient] = APIClient,
        property_api: type[PropertyAPI] = PropertyAPI,
        category_api: type[CategoryAPI] = CategoryAPI,
        provider_api: type[ProviderAPI] = ProviderAPI,
        meter_api: type[MeterAPI] = MeterAPI,
        meter_readings_api: type[MeterReadingAPI] = MeterReadingAPI,
        account_number_api: type[AccountNumberAPI] = AccountNumberAPI,
        tariff_api: type[TariffAPI] = TariffAPI,
        invoice_api: type[InvoiceAPI] = InvoiceAPI,
    ):
        self.property_api = property_api()
        self.category_api = category_api()
        self.provider_api = provider_api()
        self.account_number_api = account_number_api()
        self.meter_api = meter_api()
        self.meter_readings_api = meter_readings_api()
        self.tariff_api = tariff_api()
        self.invoice_api = invoice_api()
        self.is_running = True
        self.username: str = ""
        self.api = api(session)
        self.error_message: str = ""
        self._current_property: PropertyResponse | None = None

    def logout(self):
        self.api.logout()

    def connect_to_server(self):
        response = self.api.get_me()
        self.username = response.json()["username"]

    def login(self, payload: dict):
        response = self.api.login(payload=payload)
        self.username = response.json()["username"]

    @property
    def properties(self):
        return self.property_api.list()

    @property
    def current_property(self) -> PropertyResponse | None:
        return self._current_property

    @current_property.setter
    def current_property(self, property: PropertyResponse | None):
        if not isinstance(property, (PropertyResponse, NoneType)):
            raise TypeError(
                "Невідповідність типів. Тип аргументу property має бути PropertyResponse"
            )
        self._current_property = property


# def get_context() -> AppContext:
#     return AppContext()
