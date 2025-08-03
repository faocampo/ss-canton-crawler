from pathlib import Path


def crawl(max_links=None, output_dir=Path("output")):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "result.txt").write_text(f"max_links={max_links}\n")
    print(f"Crawling with max_links={max_links}; saving to {output_dir}")
