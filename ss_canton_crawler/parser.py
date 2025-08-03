"""HTML parsing utilities."""
from typing import Dict

from bs4 import BeautifulSoup


def parse_content(html: str) -> Dict[str, str]:
    """Parse HTML content extracted from SS Canton pages.

    Parameters
    ----------
    html: str
        Raw HTML content to parse.

    Returns
    -------
    Dict[str, str]
        Mapping with the parsed data extracted from the document.
    """
    soup = BeautifulSoup(html, "html.parser")
    data = {"title": soup.title.string if soup.title else ""}
    return data
