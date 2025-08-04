"""Command line entry point leveraging the core crawler utilities."""

from __future__ import annotations

import argparse
from pathlib import Path

from . import auth, downloads, logging_config, parser
from crawler.runner import run as core_run


def run(
    username: str,
    password: str,
    base_url: str,
    output_dir: Path,
    sections: str | Path | None = None,
    max_workers: int = 4,
    max_links: int | None = None,
) -> None:
    """Execute the crawler workflow.

    When ``sections`` is provided the full crawling engine from the ``crawler``
    package is invoked to traverse all links listed in that file.  Otherwise a
    single page at ``base_url`` is downloaded and parsed.

    Parameters
    ----------
    username:
        Login username.
    password:
        Login password.
    base_url:
        Base URL of the SS Canton site.
    output_dir:
        Directory where documents and parsed data will be stored.
    sections:
        Optional path to a file containing initial sections to crawl. Both
        relative and absolute paths are supported.
    max_workers:
        Number of worker threads for the full crawler.
    max_links:
        Optional limit of total links visited by the full crawler.
    """

    logging_config.setup_logging()
    session = auth.login(username, password, base_url)

    output_dir.mkdir(parents=True, exist_ok=True)

    if sections:
        sections_path = Path(sections).expanduser().resolve()
        core_run(
            base_url,
            str(sections_path),
            max_workers=max_workers,
            max_links=max_links,
            session=session,
        )
        return

    response_path = output_dir / "page.html"
    downloads.download_file(f"{base_url}/page", session, response_path)
    parsed = parser.parse_content(response_path.read_text(encoding="utf-8"))
    (output_dir / "data.txt").write_text(str(parsed), encoding="utf-8")


def main() -> None:
    """CLI entry point for the crawler."""

    argp = argparse.ArgumentParser(description="SS Canton crawler")
    argp.add_argument("--user", required=True, help="username for authentication")
    argp.add_argument("--password", required=True, help="password for authentication")
    argp.add_argument("--base-url", default="https://ss-canton.example.com", help="base URL of the site")
    argp.add_argument("--output", default="output", help="destination directory")
    argp.add_argument("--sections", help="file with initial sections to crawl")
    argp.add_argument("--max-workers", type=int, default=4, help="number of worker threads")
    argp.add_argument("--max-links", type=int, help="limit the number of visited links")
    args = argp.parse_args()

    run(
        args.user,
        args.password,
        args.base_url,
        Path(args.output),
        sections=Path(args.sections) if args.sections else None,
        max_workers=args.max_workers,
        max_links=args.max_links,
    )


if __name__ == "__main__":
    main()
