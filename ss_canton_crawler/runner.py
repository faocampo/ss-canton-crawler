"""Runner module orchestrating the SS Canton crawler."""
import argparse
from pathlib import Path

from . import auth, downloads, logging_config, parser


def run(username: str, password: str, base_url: str, output_dir: Path) -> None:
    """Execute the crawler workflow.

    Parameters
    ----------
    username: str
        Login username.
    password: str
        Login password.
    base_url: str
        Base URL of the SS Canton site.
    output_dir: Path
        Directory where documents and parsed data will be stored.
    """
    logging_config.setup_logging()
    session = auth.login(username, password, base_url)
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
    args = argp.parse_args()

    run(args.user, args.password, args.base_url, Path(args.output))


if __name__ == "__main__":
    main()
