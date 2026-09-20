from .base import BaseResourceAPI
from .config import ACCOUNT_NUMBERS_URL
from .models import (
    AccountNumberCreate,
    AccountNumberResponse,
    AccountNumberUpdate,
)


class AccountNumberAPI(
    BaseResourceAPI[
        AccountNumberCreate,
        AccountNumberUpdate,
        AccountNumberResponse,
    ]
):
    """API для роботи з особовими рахунками."""

    endpoint = ACCOUNT_NUMBERS_URL
    response_model = AccountNumberResponse
