from abc import ABC, abstractmethod

from ..context import AppContext


class BaseScreen(ABC):
    def __init__(self, context: AppContext):
        self.context = context

    @abstractmethod
    def render(self) -> str:
        """
        Малює екран за допомогою rich / inquirerpy.
        Повертає рядок-ідентифікатор наступного екрану (наприклад, 'main_menu').
        """
