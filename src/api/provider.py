from .base import BaseResourceAPI
from .config import PROVIDERS_URL
from .models import ProviderCreate, ProviderResponse, ProviderUpdate


class ProviderAPI(BaseResourceAPI[ProviderCreate, ProviderUpdate, ProviderResponse]):
    """API для роботи з постачальниками."""

    endpoint = PROVIDERS_URL
    response_model = ProviderResponse
