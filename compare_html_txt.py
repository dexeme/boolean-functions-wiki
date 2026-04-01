from __future__ import annotations

import sys
from pathlib import Path

DATA_DIR: str = "data"
TXT_DIR: str = "summarized-data"


def list_files(directory: str, suffix: str) -> dict[str, Path]:
    base = Path(directory)
    if not base.is_dir():
        return {}
    return {path.stem: path for path in base.iterdir() if path.suffix == suffix}


def compare_html_and_txt() -> tuple[list[str], list[str]]:
    html_files = list_files(DATA_DIR, ".html")
    txt_files = list_files(TXT_DIR, ".txt")

    missing_txt = sorted(stem for stem in html_files if stem not in txt_files)
    missing_html = sorted(stem for stem in txt_files if stem not in html_files)
    return missing_txt, missing_html


def main() -> None:
    missing_txt, missing_html = compare_html_and_txt()

    print(f"HTML without TXT: {len(missing_txt)}")
    for stem in missing_txt:
        print(stem)

    print(f"TXT without HTML: {len(missing_html)}")
    for stem in missing_html:
        print(stem)

    if missing_txt or missing_html:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
