APP_NAME = "UtilityHomeCLI"

# Authentication endpoints are intentionally kept configurable because they are
# not described by the supplied OpenAPI document.
IP_ADDRESS = "192.168.0.111"
BASE_URL = f"http://{IP_ADDRESS}:8000/api"
REGISTER_URL = f"{BASE_URL}/users/register/"
LOGIN_URL = f"{BASE_URL}/users/login/"
LOGOUT_URL = f"{BASE_URL}/users/logout/"
CSRF_URL = f"{BASE_URL}/users/csrf/"
ME_URL = f"{BASE_URL}/users/me/"
RESEND_VERIFICATION_URL = f"{BASE_URL}/users/resend-verification/"

PROPERTIES_URL = f"{BASE_URL}/properties/my-properties/"
PROVIDERS_URL = f"{BASE_URL}/properties/providers/"
CATEGORIES_URL = f"{BASE_URL}/tariffs/categories/"
ACCOUNT_NUMBERS_URL = f"{BASE_URL}/properties/accounts/"
METERS_URL = f"{BASE_URL}/meters/meters/"
METER_READINGS_URL = f"{BASE_URL}/meters/readings/"
TARIFFS_URL = f"{BASE_URL}/tariffs/tariffs/"
BENEFITS_URL = f"{BASE_URL}/tariffs/benefits/"
