from .base import BaseResourceAPI
from .config import INVOICES_URL
from .utility_models import InvoiceCreate, InvoiceResponse, InvoiceUpdate


class InvoiceAPI(BaseResourceAPI[InvoiceCreate, InvoiceUpdate, InvoiceResponse]):
    """API for invoice CRUD operations."""

    endpoint = INVOICES_URL
    response_model = InvoiceResponse
