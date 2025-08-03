"""Network-related functions for the Canton crawler."""

import logging
from pathlib import Path
from typing import Optional

import requests

from .logging_config import configure_logging
from .utils import retry

configure_logging()

logger = logging.getLogger(__name__)


@retry((requests.RequestException,))
def login(session: requests.Session, url: str, payload: dict) -> requests.Response:
    """Perform login to the given URL with provided payload."""
    logger.info("Starting login to %s", url)
    response = session.post(url, data=payload)
    response.raise_for_status()
    logger.info("Login successful to %s", url)
    return response


@retry((requests.RequestException,))
def crawl(session: requests.Session, url: str) -> str:
    """Crawl the given URL and return its text content."""
    logger.info("Starting crawl of %s", url)
    response = session.get(url)
    response.raise_for_status()
    logger.info("Finished crawl of %s", url)
    return response.text


@retry((requests.RequestException,))
def download_file(
    session: requests.Session, url: str, dest: Path
) -> Optional[Path]:
    """Download file from URL and save to destination path."""
    logger.info("Downloading file from %s", url)
    response = session.get(url)
    response.raise_for_status()
    dest.write_bytes(response.content)
    logger.info("File downloaded to %s", dest)
    return dest
