from pathlib import Path
import os

from ss_canton_crawler import runner


def _dummy_login(user, password, base_url):
    return object()


def test_run_accepts_relative_sections_path(tmp_path, monkeypatch):
    sections_file = tmp_path / "sections.txt"
    sections_file.write_text("home", encoding="utf-8")

    called = {}

    def fake_core_run(base_url, sections_file_arg, **kwargs):
        called["path"] = sections_file_arg

    monkeypatch.setattr(runner, "core_run", fake_core_run)
    monkeypatch.setattr(runner.auth, "login", _dummy_login)

    cwd = Path.cwd()
    os.chdir(tmp_path)
    try:
        runner.run("u", "p", "http://example.com", tmp_path, sections="sections.txt")
    finally:
        os.chdir(cwd)

    assert called["path"] == str(sections_file)


def test_run_accepts_absolute_sections_path(tmp_path, monkeypatch):
    sections_file = tmp_path / "sections.txt"
    sections_file.write_text("home", encoding="utf-8")

    called = {}

    def fake_core_run(base_url, sections_file_arg, **kwargs):
        called["path"] = sections_file_arg

    monkeypatch.setattr(runner, "core_run", fake_core_run)
    monkeypatch.setattr(runner.auth, "login", _dummy_login)

    runner.run("u", "p", "http://example.com", tmp_path, sections=sections_file)

    assert called["path"] == str(sections_file)
