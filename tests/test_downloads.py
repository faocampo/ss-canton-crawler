import hashlib

from crawler.downloads import _sha256sum, download_file


class DummyResponse:
    def __init__(self, content: bytes):
        self.content = content

    def raise_for_status(self) -> None:
        pass


class DummySession:
    def __init__(self, content: bytes):
        self.content = content

    def get(self, url: str) -> DummyResponse:
        return DummyResponse(self.content)


def test_sha256sum(tmp_path):
    file = tmp_path / "data.txt"
    file.write_text("hello", encoding="utf-8")
    assert _sha256sum(file) == hashlib.sha256(b"hello").hexdigest()


def test_download_file_saves_and_deduplicates(tmp_path):
    session = DummySession(b"filecontent")
    counter = {}
    path1 = download_file(session, "http://example.com/file.txt", "sec", str(tmp_path), counter)
    assert path1.exists()
    assert counter["sec"] == 1
    path2 = download_file(session, "http://example.com/file.txt", "sec", str(tmp_path), counter)
    assert path2 == path1
    assert counter["sec"] == 1
