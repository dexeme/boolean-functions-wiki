from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

import google.generativeai as genai

from llm_service import PagePayload, request_batch
from postprocess import ConceptsFile, GeminiBatchResponse, PagesFile, merge_gemini_output, parse_and_format_json

JSON_DIR: str = "jsons"
TXT_DIR: str = "summarized-data"
CONCEPTS_PATH: str = os.path.join(JSON_DIR, "concepts.json")
CONCEPTS_TXT_PATH: str = os.path.join(JSON_DIR, "concepts.txt")
PAGES_PATH: str = os.path.join(JSON_DIR, "pages.json")
ROOT_TITLE: str = "Boolean Functions"
MODEL_NAME: str = "gemini-3-flash-preview"

api_key: str | None = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=api_key)


def ensure_data_dir() -> None:
    os.makedirs(JSON_DIR, exist_ok=True)


def load_json_file(path: str, default: Any) -> Any:
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_file(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_concepts_txt(path: str, concepts: dict[str, dict[str, list[str]]]) -> None:
    ordered = sorted(concepts.keys())
    with open(path, "w", encoding="utf-8") as f:
        f.write(", ".join(ordered))


def list_txt_files() -> list[str]:
    txt_dir: Path = Path(TXT_DIR)
    if not txt_dir.is_dir():
        return []
    return sorted(str(path) for path in txt_dir.iterdir() if path.suffix == ".txt")


def parse_range_argument(value: str, total_files: int) -> tuple[int, int]:
    if not value:
        return 0, total_files

    if "-" not in value:
        index: int = int(value) - 1
        return index, index + 1

    start_text, end_text = value.split("-", 1)
    start: int = int(start_text) - 1 if start_text else 0
    end: int = int(end_text) if end_text else total_files
    return max(start, 0), min(end, total_files)


def parse_selection_argument(value: str, total_files: int) -> list[int]:
    if not value:
        return list(range(total_files))

    tokens = value.split()
    selected: set[int] = set()

    for token in tokens:
        if "-" in token:
            start_text, end_text = token.split("-", 1)
            start_idx = int(start_text) - 1 if start_text else 0
            end_idx = int(end_text) - 1 if end_text else total_files - 1
            start_idx = max(0, start_idx)
            end_idx = min(total_files - 1, end_idx)
            if start_idx <= end_idx:
                for idx in range(start_idx, end_idx + 1):
                    selected.add(idx)
        else:
            idx = int(token) - 1
            if 0 <= idx < total_files:
                selected.add(idx)

    return sorted(selected)


def initialize_state() -> tuple[ConceptsFile, PagesFile]:
    graph: ConceptsFile = load_json_file(CONCEPTS_PATH, {"concepts": []})
    page_index: PagesFile = load_json_file(PAGES_PATH, {"pages": []})

    if not isinstance(graph, dict):
        graph = {"concepts": {}}
    if "concepts" not in graph:
        graph["concepts"] = {}
    if isinstance(graph["concepts"], list):
        legacy_map: dict[str, dict[str, list[str]]] = {}
        for item in graph["concepts"]:
            title = item.get("title", "")
            if title:
                legacy_map[title] = {"dependencies": []}
        graph["concepts"] = legacy_map
    if not isinstance(graph["concepts"], dict):
        graph["concepts"] = {}

    if not isinstance(page_index, dict):
        page_index = {"pages": []}
    if "pages" not in page_index or not isinstance(page_index["pages"], list):
        page_index["pages"] = []
    normalized_pages: list[dict[str, Any]] = []
    for page in page_index["pages"]:
        if not isinstance(page, dict):
            continue
        title = str(page.get("title", "")).strip()
        if not title:
            continue
        normalized_pages.append(
            {
                "title": title,
                "url": str(page.get("url", "")).strip(),
                "concepts": page.get("concepts", []) if isinstance(page.get("concepts", []), list) else [],
            }
        )
    page_index["pages"] = normalized_pages

    if ROOT_TITLE not in graph["concepts"]:
        graph["concepts"][ROOT_TITLE] = {"dependencies": []}

    return graph, page_index


def build_pages_index(txt_files: list[str]) -> PagesFile:
    pages: list[dict[str, Any]] = []
    for filepath in txt_files:
        fallback_title: str = os.path.splitext(os.path.basename(filepath))[0]
        href, url, title, _text = read_clean_txt(filepath)
        pages.append(
            {
                "title": title or href or fallback_title,
                "url": url,
                "concepts": [],
            }
        )
    return {"pages": pages}


def merge_pages_accumulative(existing: PagesFile, incoming: PagesFile) -> PagesFile:
    by_title: dict[str, dict[str, Any]] = {page["title"]: page for page in existing["pages"]}
    for page in incoming["pages"]:
        title = page["title"]
        if title not in by_title:
            by_title[title] = page
    return {"pages": list(by_title.values())}


def read_clean_txt(filepath: str) -> tuple[str, str, str, str]:
    content: str = Path(filepath).read_text(encoding="utf-8").strip()
    if not content:
        return "", "", "", ""

    lines: list[str] = [line.strip() for line in content.splitlines() if line.strip()]

    # Preferred format (multiline header):
    # line 1: title (or href legacy), line 2: url, remaining: text
    if len(lines) >= 2 and lines[1].startswith(("http://", "https://")):
        raw_title = lines[0]
        url = lines[1]
        body = "\n".join(lines[2:]).strip()
        href = raw_title
        if raw_title.startswith("/"):
            href = raw_title[1:]
        if " " in href and url:
            parsed = urlparse(url)
            href = unquote(parsed.path.lstrip("/"))
        title = raw_title.replace("_", " ").strip()
        return href, url, title, body

    # Fallback format (single line):
    # title = text before first http
    # url   = first http token until first whitespace
    # body  = remaining text after url
    first_http = content.find("http")
    if first_http == -1:
        title = content
        return "", "", title, ""

    raw_title = content[:first_http].strip()
    after_http = content[first_http:]
    url = after_http.split(" ", 1)[0].strip()
    body = after_http[len(url):].strip()

    parsed = urlparse(url)
    href = unquote(parsed.path.lstrip("/")) if parsed.path else raw_title.replace(" ", "_")
    title = raw_title if raw_title else href.replace("_", " ")
    return href, url, title, body


def build_page_payload(filepath: str) -> PagePayload:
    source_file: str = os.path.basename(filepath)
    href, url, title, text = read_clean_txt(filepath)
    return {
        "href": href,
        "url": url,
        "title": title or os.path.splitext(source_file)[0],
        "source_file": source_file,
        "text": text[:30000],
    }


def main() -> None:
    graph_state, existing_pages = initialize_state()
    txt_files: list[str] = list_txt_files()
    selection_arg: str = sys.argv[1] if len(sys.argv) > 1 else ""
    selected_indexes = parse_selection_argument(selection_arg, len(txt_files))
    selected_files: list[str] = [txt_files[i] for i in selected_indexes]
    if not selected_files:
        print("No input TXT files selected.")
        return

    incoming_pages: PagesFile = build_pages_index(selected_files)
    page_state: PagesFile = merge_pages_accumulative(existing_pages, incoming_pages)
    ensure_data_dir()
    save_json_file(PAGES_PATH, page_state)

    batch_payload: list[PagePayload] = [build_page_payload(filepath) for filepath in selected_files]

    print(f"Processing {len(selected_files)} pages in one Gemini request...")
    raw_response: str = request_batch(MODEL_NAME, graph_state["concepts"], batch_payload)
    response_data_raw, formatted_json = parse_and_format_json(raw_response)
    response_data: GeminiBatchResponse = response_data_raw
    merge_gemini_output(graph_state, page_state, response_data)

    save_json_file(CONCEPTS_PATH, graph_state)
    save_concepts_txt(CONCEPTS_TXT_PATH, graph_state["concepts"])
    save_json_file(PAGES_PATH, page_state)
    print(formatted_json)


if __name__ == "__main__":
    main()
