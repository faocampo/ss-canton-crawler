import re
from html import unescape
import unicodedata
from typing import Optional

from bs4 import BeautifulSoup

MENU_CLASSES = {
    "nav",
    "navigation",
    "navbar",
    "menu",
    "sidebar",
    "header",
    "footer",
}

def extract_text(html: str) -> str:
    """Return clean text extracted from ``html``.

    The function removes script, style, anchor and image tags. It also drops
    elements that look like navigation menus based on common CSS classes.
    Remaining text is normalised by decoding HTML entities, standardising
    unicode representation and collapsing consecutive whitespace.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove script and style elements entirely
    for tag in soup(["script", "style"]):
        tag.decompose()

    # Replace links with their contained text and drop images
    for tag in soup.find_all("a"):
        tag.unwrap()
    for tag in soup.find_all("img"):
        tag.decompose()

    # Remove common navigation/menu containers
    for tag in soup.find_all(class_=lambda c: c and any(cls in MENU_CLASSES for cls in c.split())):
        tag.decompose()

    # Get text and normalise encoding and whitespace
    text = soup.get_text(separator=" ")
    text = unescape(text)
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
