from loguru import logger

from .base import BaseResourceAPI
from .config import TARIFFS_URL
from .utility_models import TariffChange, TariffCreate, TariffResponse, TariffUpdate


class TariffAPI(BaseResourceAPI[TariffCreate, TariffUpdate, TariffResponse]):
    """API for tariff CRUD operations."""

    endpoint = TARIFFS_URL
    response_model = TariffResponse

    def change_tariff(self, data: TariffChange):
        url = f"{self.endpoint}{data.tariff_id}/update-rate/"
        body = data.model_dump(mode="json")
        logger.debug(body)
        response = self.client.request("POST", url, json=body)
        return response
