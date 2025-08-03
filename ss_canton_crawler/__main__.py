import argparse
from concurrent.futures import ThreadPoolExecutor
from .crawler import crawl


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple Canton crawler")
    parser.add_argument("urls", nargs="+", help="URLs to crawl")
    parser.add_argument(
        "--threads",
        type=int,
        default=1,
        help="Number of worker threads to use",
    )
    args = parser.parse_args()

    if args.threads > 1:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            executor.map(crawl, args.urls)
    else:
        for url in args.urls:
            crawl(url)


if __name__ == "__main__":
    main()
