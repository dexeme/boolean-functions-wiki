from __future__ import annotations

import csv
from pathlib import Path
import re


_CITE_RE = re.compile(r":cite:[pt]:`([^`]+)`")
_DIRECTIVE_RE = re.compile(r"\s*\.\.\s+(csv-table|lazychunks|references)::")
_OPTION_RE = re.compile(r"\s*:([A-Za-z0-9_-]+):\s*(.*?)\s*$")


def _citation_keys_from_text(text: str) -> list[str]:
    keys: list[str] = []
    for match in _CITE_RE.finditer(text):
        keys.extend(key.strip() for key in match.group(1).split(",") if key.strip())
    return keys


def _append_unique_lower(keys: list[str], seen: set[str], values: list[str]) -> None:
    for key in values:
        lowered = key.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        keys.append(lowered)


def _resolve_csv_path(src_dir: Path, doc_dir: Path, value: str) -> Path:
    rel = Path(value)
    candidates = [
        doc_dir / rel,
        src_dir / "content" / "tables" / rel,
        src_dir / "tables" / rel,
        src_dir / "content" / rel,
        src_dir / "pages" / rel,
        src_dir / rel,
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return candidates[0]


def _citation_keys_from_csv(csv_path: Path) -> list[str]:
    try:
        with csv_path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.reader(handle))
    except OSError:
        return []

    keys: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for cell in row:
            _append_unique_lower(keys, seen, _citation_keys_from_text(cell))
    return keys


def _collect_reference_keys(app, docname: str, text: str) -> list[str]:
    src_dir = Path(app.srcdir)
    doc_dir = (src_dir / docname).parent
    keys: list[str] = []
    seen: set[str] = set()
    seen_csvs: set[Path] = set()
    lines = text.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i]
        _append_unique_lower(keys, seen, _citation_keys_from_text(line))
        directive = _DIRECTIVE_RE.match(line)
        if not directive or directive.group(1) not in {"csv-table", "lazychunks"}:
            i += 1
            continue

        base_indent = len(line) - len(line.lstrip(" \t"))
        option_name = "file" if directive.group(1) == "csv-table" else "csv"
        csv_path: Path | None = None
        i += 1
        while i < len(lines):
            cur = lines[i]
            cur_stripped = cur.strip()
            cur_indent = len(cur) - len(cur.lstrip(" \t"))
            if cur_stripped and cur_indent <= base_indent:
                break
            _append_unique_lower(keys, seen, _citation_keys_from_text(cur))
            option = _OPTION_RE.match(cur)
            if option and option.group(1) == option_name:
                csv_path = _resolve_csv_path(src_dir, doc_dir, option.group(2).strip())
            i += 1

        if csv_path is None:
            continue
        normalized = csv_path.resolve()
        if normalized in seen_csvs:
            continue
        seen_csvs.add(normalized)
        _append_unique_lower(keys, seen, _citation_keys_from_csv(csv_path))

    return keys


def _references_block(keys: list[str], indent: str) -> list[str]:
    if not keys:
        return []

    quoted_keys = ", ".join(f'"{key}"' for key in keys)
    return [
        f"{indent}.. bibliography::",
        f"{indent}    :filter: key in {{{quoted_keys}}}",
    ]


def _replace_references_directives(app, docname, source) -> None:
    text = source[0]
    keys = _collect_reference_keys(app, docname, text)
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    changed = False

    while i < len(lines):
        line = lines[i]
        directive = _DIRECTIVE_RE.match(line)
        if not directive or directive.group(1) != "references":
            out.append(line)
            i += 1
            continue

        changed = True
        base_indent = len(line) - len(line.lstrip(" \t"))
        indent = line[:base_indent]
        out.extend(_references_block(keys, indent))
        i += 1
        while i < len(lines):
            cur = lines[i]
            cur_stripped = cur.strip()
            cur_indent = len(cur) - len(cur.lstrip(" \t"))
            if cur_stripped and cur_indent <= base_indent:
                break
            i += 1

    if not changed:
        return

    rewritten = "\n".join(out)
    if text.endswith("\n"):
        rewritten += "\n"
    source[0] = rewritten


def setup(app):
    app.connect("source-read", _replace_references_directives)
    return {"version": "0.1", "parallel_read_safe": True, "parallel_write_safe": True}
