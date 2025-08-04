"""HTML parsing utilities relying on the core :mod:`crawler` package."""

from __future__ import annotations

from typing import Dict

from bs4 import BeautifulSoup

from crawler.parser import extract_text

__all__ = ["parse_content"]


def parse_content(html: str) -> Dict[str, str]:
    """Parse HTML content extracted from SS Canton pages.

    The function builds upon :func:`crawler.parser.extract_text` to obtain a
    cleaned representation of the document while also returning the page title
    for convenience.

    Parameters
    ----------
    html:
        Raw HTML content to parse.

    Returns
    -------
    Dict[str, str]
        Mapping with the parsed data extracted from the document. Contains at
        least ``title`` and ``text`` keys.
    """

    soup = BeautifulSoup(html, "html.parser")
    data = {
        "title": soup.title.string if soup.title else "",
        "text": extract_text(html),
    }
    return data
