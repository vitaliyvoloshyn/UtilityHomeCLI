APP_NAME = "UtilityHomeCLI"

# Authentication endpoints are intentionally kept configurable because they are
# not described by the supplied OpenAPI document.
IP_ADDRESS = "127.0.0.1"
BASE_URL = f"http://{IP_ADDRESS}:8000/api"
REGISTER_URL = f"{BASE_URL}/users/register/"
LOGIN_URL = f"{BASE_URL}/users/login/"
LOGOUT_URL = f"{BASE_URL}/users/logout/"
CSRF_URL = f"{BASE_URL}/users/csrf/"
ME_URL = f"{BASE_URL}/users/me/"
RESEND_VERIFICATION_URL = f"{BASE_URL}/users/resend-verification/"

PROPERTIES_URL = f"{BASE_URL}/my-properties/"
PROVIDERS_URL = f"{BASE_URL}/providers/"
CATEGORIES_URL = f"{BASE_URL}/categories/"
ACCOUNT_NUMBERS_URL = f"{BASE_URL}/accounts/"
METERS_URL = f"{BASE_URL}/meters/"
METER_READINGS_URL = f"{BASE_URL}/readings/"
TARIFFS_URL = f"{BASE_URL}/tariffs/"
BENEFITS_URL = f"{BASE_URL}/benefits/"
INVOICES_URL = f"{BASE_URL}/invoices/"
