from pathlib import Path
from typing import Optional

from crawler.parser import extract_text


def save_section_text(section: str, html: str, test: bool = False) -> Path:
    """Parse ``html`` and store the cleaned text for ``section``.

    When ``test`` is True the file is written under ``test_results/textos``;
    otherwise under ``textos``.
    The directory is created if it does not exist and the path of the written
    file is returned.
    """
    text = extract_text(html)
    base_dir = Path("test_results/textos" if test else "textos")
    base_dir.mkdir(parents=True, exist_ok=True)
    file_path = base_dir / f"{section}.txt"
    file_path.write_text(text, encoding="utf-8")
    return file_path


if __name__ == "__main__":  # pragma: no cover
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Process HTML and save text")
    parser.add_argument("section", help="Section name to use for the output file")
    parser.add_argument("html", help="HTML content to process")
    parser.add_argument("--test", action="store_true", help="Use test output directory")
    args = parser.parse_args()

    path = save_section_text(args.section, args.html, test=args.test)
    sys.stdout.write(str(path))
