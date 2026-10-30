from .base import BaseResourceAPI
from .config import PAYMENTS_URL
from .models import (
    PaymentUpdate, PaymentResponse, PaymentCreate
)


class PaymentAPI(
    BaseResourceAPI[
        PaymentUpdate, PaymentResponse, PaymentCreate
    ]
):
    """API для роботи з особовими рахунками."""

    endpoint = PAYMENTS_URL
    response_model = PaymentResponse
