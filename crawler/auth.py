import json
import time
from typing import Optional

import requests
from requests import Session
from requests.exceptions import RequestException


class LoginError(Exception):
    """Raised when authentication fails due to network or credential issues."""


def login(session: Optional[Session], creds_path: str) -> Session:
    """Authenticate and return a persistent :class:`requests.Session`.

    Parameters
    ----------
    session:
        Existing session instance. If ``None`` a new session is created.
    creds_path:
        Path to a JSON file containing ``{"user": ..., "password": ...}``.

    Returns
    -------
    requests.Session
        Authenticated session with cookies persisted.

    Raises
    ------
    ValueError
        If the credentials file is missing or malformed.
    LoginError
        If authentication fails after retries.
    """
    session = session or requests.Session()

    # Load credentials
    try:
        with open(creds_path, "r", encoding="utf-8") as f:
            creds = json.load(f)
        username = creds["user"]
        password = creds["password"]
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid credentials file") from exc

    url = "https://simplesolutions.com.ar/elcanton/"
    payload = {"username": username, "password": password}

    max_attempts = 5
    backoff = 1.0

    for attempt in range(1, max_attempts + 1):
        try:
            response = session.post(url, data=payload, timeout=10)
            response.raise_for_status()
            return session
        except RequestException as exc:
            if attempt == max_attempts:
                raise LoginError("Authentication failed") from exc
            time.sleep(backoff)
            backoff *= 2


