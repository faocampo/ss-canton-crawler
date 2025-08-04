"""Simple URL crawler built upon the core parser utilities."""

from __future__ import annotations

import requests

from crawler.parser import extract_text

__all__ = ["crawl"]


def crawl(url: str) -> None:
    """Fetch ``url`` and print the cleaned text extracted from its HTML."""
    response = requests.get(url)
    response.raise_for_status()
    print(extract_text(response.text))
