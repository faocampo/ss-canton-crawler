"""Authentication utilities for SS Canton crawler."""

import requests


def login(username: str, password: str, base_url: str) -> requests.Session:
    """Authenticate against the SS Canton service.

    Parameters
    ----------
    username: str
        Account username.
    password: str
        Account password.
    base_url: str
        Base URL of the SS Canton service.

    Returns
    -------
    requests.Session
        Authenticated session ready to perform subsequent requests.

    Raises
    ------
    requests.HTTPError
        If the authentication request fails.
    """
    session = requests.Session()
    response = session.post(f"{base_url}/login", data={"user": username, "pass": password})
    response.raise_for_status()
    return session
