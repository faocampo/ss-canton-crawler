import argparse
from pathlib import Path

from engine import crawl


def main():
    parser = argparse.ArgumentParser(description="SS Canton crawler")
    parser.add_argument(
        "--test",
        type=int,
        metavar="N",
        help="Run in test mode with a limit of N links.",
    )
    args = parser.parse_args()

    output_dir = Path("output")
    max_links = None
    if args.test is not None:
        max_links = args.test
        output_dir = Path("test_results") / output_dir
        print(f"[TEST MODE] max_links={max_links}, output -> {output_dir}")

    crawl(max_links=max_links, output_dir=output_dir)


if __name__ == "__main__":
    main()
