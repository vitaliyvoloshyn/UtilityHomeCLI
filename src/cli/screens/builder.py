from ..context import AppContext
from .base import Screen
from .components import ChoiceMenu, InputComponent, LogoutExitMenu, MainHeader


class BaseBuilder:
    def __init__(self):
        self.screen: Screen = Screen()

    def add_main_header(self, username: str):
        self.screen.add(MainHeader(username))
        return self

    def add_logout_exit_menu(self):
        self.screen.add(LogoutExitMenu())
        return self

    def add_choice_menu(
        self, items: list[dict[str, str]], add_logout_exit_items: bool = True
    ):
        """Приймає список типу
        [
            {"name": "Зареєструватися", "value": "registr"},
            {"name": "Авторизуватися", "value": "login"},
        ]
        """
        self.screen.add(ChoiceMenu(items, add_logout_exit_items))
        return self

    def add_input_component(self, messages: dict[str, str]):
        """Приймає словник та повертає цей же словник, але замість значень підставляє значення, які ввів юзер.
        Value вхідного словника це меседжі, які будуть показані юзеру для введення даних"""
        self.screen.add(InputComponent(messages))
        return self

    def build(self, context: AppContext) -> Screen:
        self.screen._set_context(context)
        return self.screen


builder = BaseBuilder()
