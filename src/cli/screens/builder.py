from copy import deepcopy

from ..context import AppContext
from .base import Screen
from .components import (
    AppHeader,
    ChoiceMenu,
    InputComponent,
    MenuHeaderComponent,
    TextLabel,
)


class BaseBuilder:
    def __init__(self):
        self.screen: Screen = Screen()

    def reset(self):
        self.screen = Screen()

    def add_main_header(self, username: str):
        self.screen.add(AppHeader(username))
        return self

    def add_menu_header(self, title: str):
        self.screen.add(MenuHeaderComponent(title))
        return self

    # def add_logout_exit_menu(self):
    #     self.screen.add(LogoutExitMenu())
    #     return self

    def add_choice_menu(
        self,
        items: list[dict[str, str]],
        message: str = "Оберіть дію:",
        add_logout_exit_items: bool = True,
        include_back_to_main_menu: bool = True,
    ):
        """Приймає список типу
        [
            {"name": "Зареєструватися", "value": "registr"},
            {"name": "Авторизуватися", "value": "login"},
        ]
        """
        self.screen.add(
            ChoiceMenu(
                items=items,
                add_logout_exit_items=add_logout_exit_items,
                include_back_to_main_menu=include_back_to_main_menu,
                message=message,
            )
        )
        return self

    def add_input_component(self, messages: dict[str, str]):
        """Приймає словник та повертає цей же словник, але замість значень підставляє значення, які ввів юзер.
        Value вхідного словника це меседжі, які будуть показані юзеру для введення даних"""
        self.screen.add(InputComponent(messages))
        return self

    def add_text_label(self, text: str):
        self.screen.add(TextLabel(text))
        return self

    def build(self, context: AppContext) -> Screen:
        self.screen._set_context(context)
        screen_copy = deepcopy(self.screen)

        self.reset()
        return screen_copy


builder = BaseBuilder()
