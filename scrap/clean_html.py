from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen

from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.html_utils import html_to_txt_file

DATA_DIR: str = "data"
OUTPUT_DIR: str = "summarized-data"
WIKI_BASE_URL: str = "https://boolean.wiki.uib.no/"
ALL_PAGES_URL: str = "https://boolean.wiki.uib.no/Special:AllPages"


def list_html_files() -> dict[str, Path]:
    data_dir = Path(DATA_DIR)
    if not data_dir.is_dir():
        return {}
    return {path.stem: path for path in data_dir.iterdir() if path.suffix == ".html"}


def parse_range_argument(value: str, total_files: int) -> tuple[int, int]:
    if not value:
        return 0, total_files

    if "-" not in value:
        index = int(value) - 1
        return index, index + 1

    start_text, end_text = value.split("-", 1)
    start = int(start_text) - 1 if start_text else 0
    end = int(end_text) if end_text else total_files
    return max(start, 0), min(end, total_files)


def fetch_all_pages() -> list[dict[str, str]]:
    pages: list[dict[str, str]] = []
    next_url: str | None = ALL_PAGES_URL

    while next_url:
        with urlopen(next_url) as response:
            html = response.read().decode("utf-8")

        soup = BeautifulSoup(html, "html.parser")
        body = soup.select_one(".mw-allpages-body") or soup.body or soup

        for anchor in body.select("a[href]"):
            href = anchor.get("href", "").strip()
            if not href.startswith("/"):
                continue

            canonical_href = href[1:]
            title = anchor.get_text(" ", strip=True) or canonical_href
            pages.append({"title": title, "href": canonical_href, "url": urljoin(WIKI_BASE_URL, href)})

        next_link = body.select_one('a[rel="next"], a[title*="next page" i], a[aria-label*="next" i]')
        next_url = urljoin(WIKI_BASE_URL, next_link["href"]) if next_link and next_link.get("href") else None

    return pages


def download_missing_htmls(pages: list[dict[str, str]], existing_files: dict[str, Path]) -> list[Path]:
    data_dir = Path(DATA_DIR)
    data_dir.mkdir(parents=True, exist_ok=True)

    downloaded: list[Path] = []
    for page in pages:
        href = page["href"]
        if href in existing_files:
            continue

        html_path = data_dir / f"{href}.html"
        print(f"missing: {href}")
        with urlopen(page["url"]) as response:
            html_path.write_text(response.read().decode("utf-8"), encoding="utf-8")
        downloaded.append(html_path)

    return downloaded


def clean_html_files(page_records: list[dict[str, str]], html_files_by_href: dict[str, Path]) -> list[Path]:
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    saved_files: list[Path] = []
    for page in page_records:
        html_file = html_files_by_href.get(page["href"])
        if html_file is None:
            continue

        output_path = output_dir / f"{html_file.stem}.txt"
        clean_text = html_to_txt_file(html_file, output_path)
        content = clean_text.read_text(encoding="utf-8")
        clean_text.write_text(f"{page['href']}\n{page['url']}\n{content}", encoding="utf-8")
        saved_files.append(clean_text)
    return saved_files


def main() -> None:
    existing_files = list_html_files()
    all_pages = fetch_all_pages()
    downloaded = download_missing_htmls(all_pages, existing_files)

    html_files_by_href = dict(existing_files)
    for html_path in downloaded:
        html_files_by_href[html_path.stem] = html_path

    range_arg = sys.argv[1] if len(sys.argv) > 1 else ""
    start, end = parse_range_argument(range_arg, len(all_pages))
    subset = all_pages[start:end]

    saved_files = clean_html_files(subset, html_files_by_href)
    for path in saved_files:
        print(path)


if __name__ == "__main__":
    main()
