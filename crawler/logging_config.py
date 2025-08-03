import logging


def configure_logging():
    """Configure basic logging for the crawler package."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
