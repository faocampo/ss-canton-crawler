"""Logging configuration utilities."""
import logging
from typing import Optional


def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None) -> None:
    """Configure logging for the crawler.

    Parameters
    ----------
    level: int, default ``logging.INFO``
        Logging verbosity level.
    log_file: Optional[str]
        File path to store logs. If ``None``, logs are output to stderr.
    """
    handlers = []
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    else:
        handlers.append(logging.StreamHandler())
    logging.basicConfig(level=level, handlers=handlers, format="%(levelname)s:%(name)s:%(message)s")
