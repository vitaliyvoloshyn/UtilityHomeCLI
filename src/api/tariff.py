from .base import BaseResourceAPI
from .config import TARIFFS_URL
from .utility_models import TariffCreate, TariffResponse, TariffUpdate


class TariffAPI(BaseResourceAPI[TariffCreate, TariffUpdate, TariffResponse]):
    """API for tariff CRUD operations."""

    endpoint = TARIFFS_URL
    response_model = TariffResponse
