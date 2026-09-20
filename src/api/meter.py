from .base import BaseResourceAPI
from .config import METERS_URL
from .utility_models import MeterCreate, MeterResponse, MeterUpdate


class MeterAPI(BaseResourceAPI[MeterCreate, MeterUpdate, MeterResponse]):
    """API for meter CRUD operations."""

    endpoint = METERS_URL
    response_model = MeterResponse
