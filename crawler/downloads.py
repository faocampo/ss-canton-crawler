from __future__ import annotations

import hashlib
import os
from pathlib import Path
from urllib.parse import urlparse
from typing import Dict, Optional


def _sha256sum(path: Path) -> str:
    """Return the SHA256 checksum of a file."""
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def download_file(session,
                  url: str,
                  section: str,
                  dest_dir: Optional[str],
                  counter: Dict[str, int]) -> Optional[Path]:
    """Download ``url`` using ``session`` into ``dest_dir``.

    Parameters
    ----------
    session: requests-like session with ``get`` method.
    url: URL of the file to download.
    section: Section name used to build the final file name.
    dest_dir: Directory where the file will be stored. If ``None`` the
        directory is chosen automatically: ``documentos/`` or
        ``test_results/documentos/`` depending on the ``TEST_MODE``
        environment variable.
    counter: Shared dictionary keeping track of the number of files per
        section.

    Returns
    -------
    Path to the downloaded file or ``None`` if the file already exists.
    """
    if dest_dir is None:
        base = 'test_results/documentos' if os.getenv('TEST_MODE') else 'documentos'
    else:
        base = dest_dir

    dest_path = Path(base)
    dest_path.mkdir(parents=True, exist_ok=True)

    # Determine extension from URL
    parsed = urlparse(url)
    ext = Path(parsed.path).suffix.lstrip('.')

    next_index = counter.get(section, 0) + 1
    filename = f"{section}-{next_index}.{ext}" if ext else f"{section}-{next_index}"
    file_path = dest_path / filename

    if file_path.exists():
        return file_path

    # Download the content
    response = session.get(url)
    response.raise_for_status()
    content = response.content
    file_hash = hashlib.sha256(content).hexdigest()

    # Compare with existing files using hash
    for existing in dest_path.glob('*'):
        try:
            if _sha256sum(existing) == file_hash:
                return existing
        except OSError:
            continue

    # Save file and update counter
    file_path.write_bytes(content)
    counter[section] = next_index
    return file_path
