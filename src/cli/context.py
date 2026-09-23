from ..api import PropertyResponse
from ..api import APIClient, PropertyAPI


class AppContext:
    def __init__(
            self,
            api: type[APIClient] = APIClient,
            property_api: type[PropertyAPI] = PropertyAPI,
    ):
        self.property_api = property_api()
        self.is_running = True
        self.username: str = ""
        self.api = api()
        self.error_message: str = ""
        self.current_property: PropertyResponse = None

    def logout(self):
        self.api.logout()

    def connect_to_server(self):
        response = self.api.get_me()
        self.username = response.json()["username"]

    def login(self, payload: dict):
        response = self.api.login(payload=payload)
        self.username = response.json()["username"]

    @property
    def properties(self):
        return self.property_api.list()
