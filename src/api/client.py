from __future__ import annotations

from typing import Any

import requests

from .config import (
    CSRF_URL,
    LOGIN_URL,
    LOGOUT_URL,
    ME_URL,
    REGISTER_URL,
    RESEND_VERIFICATION_URL,
)
from .credentials import get_credentials, save_credentials


class APIError(requests.HTTPError):
    """Помилка HTTP/API із збереженням відповіді сервера."""

    @property
    def status_code(self) -> int | None:
        """HTTP status code, якщо помилка містить відповідь сервера."""
        return self.response.status_code if self.response is not None else None


class AuthError(requests.HTTPError):
    @property
    def status_code(self) -> int | None:
        """HTTP status code, якщо помилка містить відповідь сервера."""
        return self.response.status_code if self.response is not None else None


class APIClient:
    """Низькорівневий HTTP-клієнт: session, auth, CSRF та запити."""

    _CSRF_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})

    def __init__(self) -> None:
        self.session = requests.Session()
        self._load_credentials()

    def _load_credentials(self) -> None:
        session_id, csrf_token = get_credentials()

        if session_id:
            self.session.cookies.set("sessionid", session_id, domain="127.0.0.1")
        if csrf_token:
            self.session.cookies.set("csrftoken", csrf_token, domain="127.0.0.1")
            self.session.headers.update({"X-CSRFToken": csrf_token})
        print("session_id", session_id, "csrf_token", csrf_token)

    def _set_csrf_header(self, token: str) -> None:
        self.session.headers.update({"X-CSRFToken": token})

    def refresh_csrf(self) -> str:
        """Отримати актуальний CSRF token та синхронізувати його із session."""
        print("Запит на токен")
        try:
            response = self.session.get(CSRF_URL)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise APIError("Не вдалося отримати CSRF token.") from exc

        token = response.cookies.get("csrftoken", domain="127.0.0.1")
        if not token:
            raise APIError("Server did not return a CSRF token", response=response)

        self._set_csrf_header(token)
        save_credentials(
            self.session.cookies.get("sessionid", domain="127.0.0.1"), token
        )
        return token

    @classmethod
    def _requires_csrf(cls, method: str) -> bool:
        return method.upper() in cls._CSRF_METHODS

    def request(
        self,
        method: str,
        url: str,
        *,
        json: Any = None,
        retry_on_csrf: bool = True,
        timeout: float = 30.0,
    ) -> requests.Response:
        """Виконати HTTP-запит із централізованою CSRF-логікою."""
        method = method.upper()
        csrf_required = self._requires_csrf(method)

        if csrf_required and "X-CSRFToken" not in self.session.headers:
            self.refresh_csrf()

        try:
            response = self.session.request(method, url, json=json, timeout=timeout)
            print("response", response.status_code)

            # Якщо отримали 403, пробуємо оновити токен ОДИН раз
            if csrf_required and response.status_code == 403 and retry_on_csrf:
                self.refresh_csrf()
                # Робимо повторний запит через сесію (вже без виклику retry_on_csrf)
                response = self.session.request(method, url, json=json, timeout=timeout)

            # Перевіряємо фінальний статус-код (викине HTTPError для >= 400)
            response.raise_for_status()

        except requests.HTTPError as exc:
            # Сюди потрапляємо, якщо raise_for_status() виявив помилку (наприклад, 400, 404, 500)
            # Тут змінна response ГАРАНТОВАНО існує
            raise AuthError(
                f"Помилка сервера під час {method} {url} -> {response.status_code}: {response.text[:500]}",
                response=response,
            ) from exc

        except requests.RequestException as exc:
            # Сюди потрапляємо в разі проблем з мережею (таймаут, відсутність інтернету)
            # Змінної response може не бути, тому не використовуємо її
            raise APIError("Помилка з'єднання з сервером.") from exc

        return response

    def register(self, payload: dict[str, Any]) -> requests.Response:
        """Зареєструвати користувача."""
        return self.request("POST", REGISTER_URL, json=payload)

    def login(self, payload: dict[str, Any]) -> requests.Response:
        """Виконати логін та зберегти отримані credentials."""
        response = self.request("POST", LOGIN_URL, json=payload)
        save_credentials(
            self.session.cookies.get("sessionid"),
            self.session.cookies.get("csrftoken"),
        )
        return response

    def get_me(self) -> requests.Response:
        """Повернути поточного користувача."""
        return self.request("GET", ME_URL)

    def resend_verification(self, email: str) -> requests.Response:
        """Повторно надіслати лист для верифікації email."""
        return self.request("POST", RESEND_VERIFICATION_URL, json={"email": email})

    def logout(self):
        return self.request("POST", LOGOUT_URL)
