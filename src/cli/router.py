import os

from ..api import APIError, AuthError
from .context import AppContext
from .screens import *

# Сюди ж імпортуєте інші екрани, наприклад, DataTableScreen


class Router:
    def __init__(self, context: AppContext):
        self.context = context
        # Реєструємо екрани: ключ — назва, значення — клас екрану
        self._screens = {
            "auth": auth_screen,
            "login": login_screen,
            # "main_menu": MainMenuScreen(self.context),
            # "api_error": APIErrorScreen(self.context),
            "menu_unauth": menu_unauth_screen,
            # "register": RegisterScreen(self.context),
            # "data_table": DataTableScreen(self.context),
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
