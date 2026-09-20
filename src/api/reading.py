from .base import BaseResourceAPI
from .config import METER_READINGS_URL
from .utility_models import MeterReadingCreate, MeterReadingResponse, MeterReadingUpdate


class MeterReadingAPI(
    BaseResourceAPI[MeterReadingCreate, MeterReadingUpdate, MeterReadingResponse]
):
    """API for meter-reading CRUD operations."""

    endpoint = METER_READINGS_URL
    response_model = MeterReadingResponse
