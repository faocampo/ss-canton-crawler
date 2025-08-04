from queue import Queue
import threading

from crawler.runner import load_sections, crawl as runner_crawl


class DummyResponse:
    def __init__(self, text: str):
        self.text = text

    def raise_for_status(self) -> None:
        pass


class DummySession:
    def __init__(self, text: str):
        self.text = text

    def get(self, url: str) -> DummyResponse:
        return DummyResponse(self.text)


def test_load_sections(tmp_path):
    file = tmp_path / "sections.txt"
    file.write_text("a\n\nb\n", encoding="utf-8")
    assert load_sections(str(file)) == ["a", "b"]


def test_crawl_enqueues_links_respecting_max(tmp_path):
    html = "<a href='p1'></a><a href='p2'></a>"
    session = DummySession(html)
    visited = {"http://example.com/start"}
    q: "Queue[tuple[str, str]]" = Queue()
    lock = threading.Lock()
    runner_crawl(session, "http://example.com/start", "sec", 2, visited, q, lock)
    assert q.get_nowait() == ("http://example.com/p1", "sec")
    assert q.empty()
    assert visited == {"http://example.com/start", "http://example.com/p1"}


def test_crawl_handles_request_errors(tmp_path):
    class ErrorSession:
        def get(self, url: str):
            raise Exception("boom")

    visited = set()
    q: "Queue[tuple[str, str]]" = Queue()
    lock = threading.Lock()
    runner_crawl(ErrorSession(), "http://example.com", "sec", None, visited, q, lock)
    assert q.empty()
    assert visited == set()
