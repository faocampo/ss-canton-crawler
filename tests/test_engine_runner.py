import os
from pathlib import Path

from engine import crawl as engine_crawl
from runner import save_section_text


def test_engine_crawl_creates_result_file(tmp_path, capsys):
    output_dir = tmp_path / "out"
    engine_crawl(max_links=5, output_dir=output_dir)
    result_file = output_dir / "result.txt"
    assert result_file.exists()
    assert result_file.read_text() == "max_links=5\n"
    captured = capsys.readouterr()
    assert f"max_links=5" in captured.out


def test_save_section_text_writes_clean_text(tmp_path, monkeypatch):
    html = "<html><body><h1>Hello</h1><script>bad()</script></body></html>"
    monkeypatch.chdir(tmp_path)
    path = save_section_text("greeting", html, test=True)
    expected_path = tmp_path / "test_results" / "textos" / "greeting.txt"
    assert path.resolve() == expected_path
    assert path.read_text(encoding="utf-8") == "Hello"
