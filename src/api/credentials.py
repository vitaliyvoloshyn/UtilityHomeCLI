from __future__ import annotations

from .config import APP_NAME


def _keyring():
    import keyring
    return keyring


def save_credentials(session_id: str | None, csrf_token: str | None) -> None:
    """Зберегти sessionid та csrftoken у Windows Credential Manager."""
    keyring = _keyring()
    if session_id:
        keyring.set_password(APP_NAME, "sessionid", session_id)
    if csrf_token:
        keyring.set_password(APP_NAME, "csrftoken", csrf_token)


def get_credentials() -> tuple[str | None, str | None]:
    """Повернути sessionid та csrftoken із Windows Credential Manager."""
    keyring = _keyring()
    return (
        keyring.get_password(APP_NAME, "sessionid"),
        keyring.get_password(APP_NAME, "csrftoken"),
    )


def clear_credentials() -> None:
    """Видалити збережені токени та сесію з Windows Credential Manager."""
    keyring = _keyring()
    for key in ("sessionid", "csrftoken"):
        try:
            keyring.delete_password(APP_NAME, key)
        except keyring.errors.PasswordDeleteError:
            pass
