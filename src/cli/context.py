from ..api import APIClient


class AppContext:
    def __init__(self, api: type[APIClient] = APIClient):
        self.is_running = True
        self.username: str = ""
        self.api = api()
        self.error_message: str = ""

    def logout(self):
        self.api.logout()

    def connect_to_server(self):
        response = self.api.get_me()
        self.username = response.json()["username"]

    def login(self, payload: dict):
        response = self.api.login(payload=payload)
        self.username = response.json()["username"]
