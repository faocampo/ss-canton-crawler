"""Utility functions for crawling the SS Canton site."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty
from typing import Iterable, List, Set, Tuple
from urllib.parse import urljoin
import threading

import requests
from bs4 import BeautifulSoup


def load_sections(file_path: str) -> List[str]:
    """Return initial section paths listed in *file_path*.

    Each non-empty line in the file is considered a relative path that
    should be crawled. Blank lines are ignored.
    """
    sections: List[str] = []
    with open(file_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                sections.append(line)
    return sections


def crawl(
    session: requests.Session,
    url: str,
    section_name: str,
    max_links: int | None,
    visited: Set[str],
    queue: "Queue[Tuple[str, str]]",
    lock: threading.Lock,
) -> None:
    """Fetch *url* and enqueue discovered links.

    Parameters
    ----------
    session:
        ``requests.Session`` used for HTTP requests.
    url:
        Absolute URL to fetch.
    section_name:
        Name of the section that produced this URL (for bookkeeping or
        logging).
    max_links:
        When not ``None`` the crawler will stop enqueuing new links once the
        total number of visited URLs reaches this value. This is useful for
        tests.
    visited:
        Shared set of URLs that have already been processed.
    queue:
        Shared queue where new URLs will be pushed for further crawling.
    lock:
        Mutex protecting access to ``visited`` and ``queue``.
    """

    try:
        response = session.get(url)
        response.raise_for_status()
    except Exception:
        return

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)

    for link in links:
        href = link["href"]
        absolute_url = urljoin(url, href)

        with lock:
            if absolute_url in visited:
                continue
            if max_links is not None and len(visited) >= max_links:
                return
            visited.add(absolute_url)
            queue.put((absolute_url, section_name))


def run(
    base_url: str,
    sections_file: str,
    max_workers: int = 4,
    max_links: int | None = None,
    session: requests.Session | None = None,
) -> None:
    """Start the crawler.

    Parameters
    ----------
    base_url:
        Base URL of the site to crawl. Section paths will be joined to this
        value using :func:`urllib.parse.urljoin`.
    sections_file:
        Path to a file listing initial sections to crawl.
    max_workers:
        Number of worker threads to spawn.
    max_links:
        Optional limit of total links to visit, used mainly for tests.
    session:
        Optional ``requests.Session`` to use for HTTP requests. When ``None`` a
        new session is created internally.
    """

    session = session or requests.Session()
    visited: Set[str] = set()
    lock = threading.Lock()
    q: "Queue[Tuple[str, str]]" = Queue()

    # Seed the queue with initial sections.
    for section in load_sections(sections_file):
        url = urljoin(base_url, section)
        visited.add(url)
        q.put((url, section))

    def worker() -> None:
        while True:
            try:
                current_url, section = q.get(timeout=0.1)
            except Empty:
                return
            crawl(session, current_url, section, max_links, visited, q, lock)
            q.task_done()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for _ in range(max_workers):
            executor.submit(worker)
        q.join()
