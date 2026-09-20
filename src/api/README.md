# API layer

API layer responsibilities:

- `client.py` — shared `requests.Session`, credentials, CSRF handling, HTTP errors and authentication requests;
- `base.py` — generic typed CRUD (`list`, `get`, `create`, `update`, `replace`, `delete`);
- resource modules — endpoint declarations and Pydantic type parameters;
- `models.py` / `utility_models.py` — request/response schemas derived from the supplied OpenAPI contract;
- `credentials.py` — Windows Credential Manager integration through `keyring`.

All resource classes receive the same `APIClient` instance. They do not create their own sessions and do not contain UI logic.

The supplied OpenAPI contract contains resources for properties, providers, categories, service accounts, meters, readings, tariffs and benefits. It does not contain separate `bills` or `payments` resources, so those endpoints are intentionally absent.
