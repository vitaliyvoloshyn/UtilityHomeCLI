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

    def top_up(self, amount: float, account_id: int):
        """
        Поповнення балансу особового рахунка
        param: amount: сума поповнення;
        param: account_id: id особового рахунка (вставляється в url)
        return: None
        """
        self.client.request(
            method="POST",
            url=f"{self.endpoint}{account_id}/top-up/",
            json={"amount": amount},
        )
