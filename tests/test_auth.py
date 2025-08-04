import json
import pytest
from requests.exceptions import RequestException

from crawler.auth import login, LoginError


class DummyResponse:
    def raise_for_status(self) -> None:
        pass


class FailThenSuccessSession:
    def __init__(self, failures: int):
        self.failures = failures

    def post(self, url: str, data: dict, timeout: int):
        if self.failures > 0:
            self.failures -= 1
            raise RequestException("fail")
        return DummyResponse()


def test_login_success_after_retries(tmp_path, monkeypatch):
    creds = tmp_path / "creds.json"
    creds.write_text(json.dumps({"user": "u", "password": "p"}))
    session = FailThenSuccessSession(2)
    monkeypatch.setattr("time.sleep", lambda x: None)
    returned = login(session, str(creds))
    assert returned is session


def test_login_invalid_credentials_file(tmp_path):
    creds = tmp_path / "bad.json"
    creds.write_text("not json")
    with pytest.raises(ValueError):
        login(None, str(creds))


def test_login_fails_after_retries(tmp_path, monkeypatch):
    creds = tmp_path / "creds.json"
    creds.write_text(json.dumps({"user": "u", "password": "p"}))

    class AlwaysFailSession:
        def post(self, url: str, data: dict, timeout: int):
            raise RequestException("fail")

    monkeypatch.setattr("time.sleep", lambda x: None)
    with pytest.raises(LoginError):
        login(AlwaysFailSession(), str(creds))
