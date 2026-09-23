import os

from ..api import APIError, AuthError
from .context import AppContext
from .screens import *

# Сюди ж імпортуєте інші екрани, наприклад, DataTableScreen


class Router:
    def __init__(self, context: AppContext):
        self.context = context
        # Реєструємо екрани: ключ — назва, значення — клас екрана
        self._screens = {
            "login": auth_screen,
            "main_menu": main_menu_screen,
            "api_error": error_screen,
            "menu_unauth": menu_unauth_screen,
            "register": register_screen,
            "data_table": dev_screen,
            "dev": dev_screen,
            "add_property": add_property_screen,
            "detail_property": property_detail_screen,
        }
        self.current_screen_name = "main_menu"

    def run(self):
        try:
            self.context.connect_to_server()
        except AuthError:
            self.current_screen_name = "menu_unauth"
        except APIError as exc:
            self.context.error_message = str(exc)
            self.current_screen_name = "api_error"

        while self.context.is_running:
            # Отримуємо об'єкт поточного екрану
            screen = self._screens.get(self.current_screen_name)

            if not screen:
                print(f"Помилка: Екран {self.current_screen_name} не знайдено.")
                break

            # Рендеримо екран і отримуємо назву наступного
            self.clear_console()
            try:
                next_screen = screen(self.context)
            except AuthError:
                next_screen = "menu_unauth"
            except APIError as exc:
                self.context.error_message = str(exc)
                next_screen = "api_error"

            if next_screen == "logout":
                self.context.logout()
                next_screen = "menu_unauth"

            if next_screen == "exit":
                self.context.is_running = False
                break

            self.current_screen_name = next_screen

    def clear_console(self):
        # os.system("cls" if os.name == "nt" else "clear")
        ...
