from .base import BaseResourceAPI
from .config import BENEFITS_URL
from .utility_models import BenefitCreate, BenefitResponse, BenefitUpdate


class BenefitAPI(BaseResourceAPI[BenefitCreate, BenefitUpdate, BenefitResponse]):
    """API for benefit CRUD operations."""

    endpoint = BENEFITS_URL
    response_model = BenefitResponse
