#!/usr/bin/env python3
"""Extract text content from downloaded Canton HTML pages.

This module provides a command line interface to iterate over HTML files
and extract the main textual content found inside ``table.contenido``
regions. It supports concurrent processing and writing to a single output
file in ``txt``, ``md`` or ``jsonl`` formats.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import html as html_module
import json
import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple
import copy

from bs4 import BeautifulSoup, Tag

LOGGER = logging.getLogger(__name__)


@dataclass
class ExtractResult:
    """Container for extracted information."""

    title: Optional[str]
    date: Optional[str]
    text: str
    used_fallback: Optional[str]


def load_html(path: Path, encoding: str) -> str:
    """Load HTML from *path* using ``encoding``.

    ``utf-8`` files may contain a BOM; this function transparently strips it.
    """

    enc = encoding
    if encoding.lower().replace("-", "") == "utf8":
        enc = "utf-8-sig"
    with path.open("r", encoding=enc, errors="replace") as handle:
        return handle.read()


def find_target_region(soup: BeautifulSoup) -> Tuple[Tag, str]:
    """Locate the region that contains the main content.

    Returns a pair ``(tag, used_fallback)`` where *used_fallback* describes
    which selector matched.
    """

    region = soup.select_one("table.contenido")
    if region:
        return region, "contenido"
    region = soup.select_one("div#news-body")
    if region:
        return region, "news-body"
    region = soup.select_one("div.novedadespop_mensaje")
    if region:
        return region, "novedadespop_mensaje"
    candidates = soup.find_all(["div", "table", "section", "article", "main", "body"])
    region = max(candidates, key=lambda t: len(t.get_text(" ", strip=True))) if candidates else soup
    return region, "largest"


def find_date(soup: BeautifulSoup) -> Optional[str]:
    """Return the text contained in ``td.novedadespop_fecha`` if present."""

    tag = soup.select_one("td.novedadespop_fecha")
    return normalize_text(tag.get_text()) if tag else None

def _cleanup_region(region: Tag) -> None:
    for tag in region.select("script,style,noscript,header,footer,nav"):
        tag.decompose()


def _get_text(node: Tag) -> str:
    """Return visible text from ``node``.

    ``<br>`` tags become newlines and common block-level tags yield a trailing
    newline so that paragraphs remain separated while inline elements do not
    introduce artificial breaks.
    """

    node = copy.copy(node)
    for br in node.find_all("br"):
        br.replace_with("\n")
    block_tags = ["p", "div", "table", "tr", "td", "li"] + [f"h{i}" for i in range(1, 7)]
    for tag in node.find_all(block_tags):
        if tag is not node:
            tag.append("\n")
    return node.get_text()


def extract_from_region(region: Tag) -> Tuple[Optional[str], str]:
    """Extract title and text from *region*.

    The function concatenates the text contents of descendant tables with
    ``role="presentation"`` in document order. When no such tables exist, the
    entire region's text is extracted.
    """

    region = copy.copy(region)  # work on a copy to avoid mutating the soup
    _cleanup_region(region)

    title_tag = region.select_one(".novedadespop_titulo")
    title = _get_text(title_tag).strip() if title_tag else None

    presentation_tables = region.select("table[role='presentation']")
    parts: List[str] = []
    if presentation_tables:
        for tbl in presentation_tables:
            parts.append(_get_text(tbl))
    else:
        parts.append(_get_text(region))
    text = "\n".join(parts)
    return title, text


def normalize_text(text: str) -> str:
    """Normalize whitespace and decode HTML entities."""

    text = html_module.unescape(text)
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_text(html: str) -> ExtractResult:
    """Return :class:`ExtractResult` for *html*.

    >>> sample = '<table class="contenido"><tr><td><div class="novedadespop_titulo">T</div><table role="presentation"><tr><td>Hi<br>there</td></tr></table></td></tr></table>'
    >>> extract_text(sample).text
    'Hi\nthere'
    """

    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:  # pragma: no cover - lxml should be available
        soup = BeautifulSoup(html, "html.parser")

    region, fallback = find_target_region(soup)
    title, text = extract_from_region(region)
    text = normalize_text(text)
    date = find_date(soup)
    LOGGER.debug("Used region: %s", fallback)
    return ExtractResult(title=title, date=date, text=text, used_fallback=fallback)

def process_file(path: Path, encoding: str) -> ExtractResult:
    try:
        html = load_html(path, encoding)
        return extract_text(html)
    except Exception as exc:  # pragma: no cover - defensive
        LOGGER.warning("Failed to process %s: %s", path, exc)
        return ExtractResult(title=None, date=None, text="", used_fallback="error")

def aggregate_and_write(results: List[Tuple[Path, ExtractResult]], out_file: Path, fmt: str) -> None:
    results.sort(key=lambda x: str(x[0]))
    out_file.parent.mkdir(parents=True, exist_ok=True)

    if fmt == "jsonl":
        with out_file.open("w", encoding="utf-8") as handle:
            for path, res in results:
                obj = {"file": str(path), "date": res.date, "title": res.title, "text": res.text}
                handle.write(json.dumps(obj, ensure_ascii=False) + "\n")
        return

    with out_file.open("w", encoding="utf-8") as handle:
        for idx, (path, res) in enumerate(results):
            meta: List[str] = []
            if res.date:
                meta.append(res.date)
            if res.title:
                meta.append(f"# {res.title}" if fmt == "md" else res.title)
            if meta:
                content = "\n".join(meta) + "\n\n" + res.text
            else:
                content = res.text
            content = content.rstrip()
            handle.write(content)
            if idx != len(results) - 1:
                handle.write("\n\n")


def iter_files(base: Path, pattern: str) -> Iterable[Path]:
    return list(base.glob(pattern))


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract Canton HTML content")
    parser.add_argument("--in", dest="input_dir", type=Path, required=True, help="Input directory")
    parser.add_argument("--out-file", dest="out_file", type=Path, required=True, help="Output file path")
    parser.add_argument("--glob", default="**/*.html", help="Glob pattern for input files")
    parser.add_argument("--format", choices=["txt", "md", "jsonl"], default="txt")
    parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--workers", type=int, default=os.cpu_count() or 1)
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format="%(levelname)s:%(message)s")

    files = iter_files(args.input_dir, args.glob)
    if not files:
        LOGGER.info("No files found for pattern %s", args.glob)
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        future_to_path = {ex.submit(process_file, path, args.encoding): path for path in files}
        results: List[Tuple[Path, ExtractResult]] = []
        for fut in concurrent.futures.as_completed(future_to_path):
            path = future_to_path[fut]
            res = fut.result()
            if res.used_fallback != "contenido":
                LOGGER.info("%s used fallback %s", path, res.used_fallback)
            results.append((path, res))

    aggregate_and_write(results, args.out_file, args.format)


if __name__ == "__main__":  # pragma: no cover
    main()
