import pytest

from crawler.utils import retry


def test_retry_eventually_succeeds(monkeypatch):
    calls = {"count": 0}

    @retry((ValueError,), tries=3, base_delay=0)
    def flaky():
        calls["count"] += 1
        if calls["count"] < 2:
            raise ValueError("fail")
        return "ok"

    monkeypatch.setattr("time.sleep", lambda x: None)
    assert flaky() == "ok"
    assert calls["count"] == 2


def test_retry_raises_after_exhausting(monkeypatch):
    @retry((RuntimeError,), tries=2, base_delay=0)
    def always_fail():
        raise RuntimeError("boom")

    monkeypatch.setattr("time.sleep", lambda x: None)
    with pytest.raises(RuntimeError):
        always_fail()
