import requests

from .config import IP_ADDRESS
from .credentials import get_credentials


def get_session() -> requests.Session:
    session = requests.Session()
    load_credentials(session)
    return session


def load_credentials(session: requests.Session) -> None:
    session_id, csrf_token = get_credentials()

    if session_id:
        session.cookies.set("sessionid", session_id, domain=IP_ADDRESS)
    if csrf_token:
        session.cookies.set("csrftoken", csrf_token, domain=IP_ADDRESS)
        session.headers.update({"X-CSRFToken": csrf_token})


session = get_session()
