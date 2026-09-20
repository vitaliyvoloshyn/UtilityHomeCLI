from .base import BaseResourceAPI
from .config import PROPERTIES_URL
from .models import PropertyCreate, PropertyResponse, PropertyUpdate


class PropertyAPI(BaseResourceAPI[PropertyCreate, PropertyUpdate, PropertyResponse]):
    """API для роботи з об'єктами нерухомості."""

    endpoint = PROPERTIES_URL
    response_model = PropertyResponse
