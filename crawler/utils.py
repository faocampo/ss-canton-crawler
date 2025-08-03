import logging
import time
from functools import wraps


logger = logging.getLogger(__name__)


def retry(exceptions, tries=3, base_delay=1):
    """Retry calling the decorated function using exponential backoff."""
    if tries < 1:
        raise ValueError("tries must be 1 or greater")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            last_exc = None
            for attempt in range(1, tries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:  # type: ignore
                    logger.error(
                        "Attempt %s/%s failed with error: %s", attempt, tries, exc
                    )
                    last_exc = exc
                    if attempt == tries:
                        break
                    time.sleep(delay)
                    delay *= 2
            # Re-raise the last exception after exhausting retries
            raise last_exc

        return wrapper

    return decorator
