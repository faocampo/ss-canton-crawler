"""Download helpers for fetching documents."""
from pathlib import Path

import requests


def download_file(url: str, session: requests.Session, destination: Path) -> Path:
    """Download a file and store it locally.

    Parameters
    ----------
    url: str
        URL of the file to download.
    session: requests.Session
        Authenticated session used to perform the request.
    destination: Path
        Location where the file will be saved.

    Returns
    -------
    Path
        Path to the downloaded file.
    """
    response = session.get(url)
    response.raise_for_status()
    destination.write_bytes(response.content)
    return destination
