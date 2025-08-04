"""Authentication helpers delegating to the core :mod:`crawler` package."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import requests

from crawler.auth import LoginError, login as _core_login

__all__ = ["login", "LoginError"]


def login(username: str, password: str, base_url: str) -> requests.Session:
    """Authenticate against the SS Canton service.

    This wrapper funnels the provided ``username`` and ``password`` through
    :func:`crawler.auth.login` so the retry and error handling logic of the
    core implementation is reused.  Credentials are written to a temporary JSON
    file compatible with the core function interface.  ``base_url`` is accepted
    for API backwards compatibility, but the underlying authentication endpoint
    is defined by the core implementation.

    Parameters
    ----------
    username:
        Account username.
    password:
        Account password.
    base_url:
        Base URL of the SS Canton service. Currently unused.

    Returns
    -------
    requests.Session
        Authenticated session ready to perform subsequent requests.
    """

    creds = {"user": username, "password": password}
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as fh:
        json.dump(creds, fh)
        creds_path = fh.name

    try:
        return _core_login(requests.Session(), creds_path)
    finally:
        Path(creds_path).unlink(missing_ok=True)
