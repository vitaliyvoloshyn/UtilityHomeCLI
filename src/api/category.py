from .base import BaseResourceAPI
from .config import CATEGORIES_URL
from .models import CategoryCreate, CategoryResponse, CategoryUpdate


class CategoryAPI(BaseResourceAPI[CategoryCreate, CategoryUpdate, CategoryResponse]):
    """API для роботи з категоріями."""

    endpoint = CATEGORIES_URL
    response_model = CategoryResponse
