from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup, Comment, Tag

from symbol_utils import replace_symbols

BLOCK_TAGS = {
    "script",
    "style",
    "noscript",
    "header",
    "footer",
    "nav",
    "aside",
    "form",
    "svg",
}

FAILED_TO_PARSE_PREFIX = "Failed to parse ("


def _extract_latex_from_math(tag: Tag) -> str:
    alttext = tag.get("alttext")
    if alttext:
        return alttext.strip()

    annotation = tag.find("annotation", attrs={"encoding": "application/x-tex"})
    if annotation and annotation.get_text(strip=True):
        return annotation.get_text(strip=True)

    data_tex = tag.get("data-mathml") or tag.get("data-tex")
    if data_tex:
        return data_tex.strip()

    alt = tag.get("alt")
    if alt:
        return alt.strip()

    text = tag.get_text(" ", strip=True)
    return text.strip()


def _extract_failed_parse_formula(text: str) -> str:
    if FAILED_TO_PARSE_PREFIX not in text:
        return text

    last_brace = text.find("{\\displaystyle")
    if last_brace != -1:
        return text[last_brace:].strip()

    return re.sub(r"^Failed to parse \([^)]*\):\s*", "", text).strip()


def _render_inline_math(node: Tag) -> str:
    pieces: list[str] = []
    for child in node.children:
        if isinstance(child, Tag):
            if child.name == "sup":
                base = pieces.pop().rstrip() if pieces else ""
                exponent = child.get_text(" ", strip=True)
                if base:
                    pieces.append(f"{base}^{{{exponent}}}")
                else:
                    pieces.append(f"^{{{exponent}}}")
            elif child.name == "sub":
                base = pieces.pop().rstrip() if pieces else ""
                subscript = child.get_text(" ", strip=True)
                if base:
                    pieces.append(f"{base}_{{{subscript}}}")
                else:
                    pieces.append(f"_{{{subscript}}}")
            else:
                pieces.append(_render_inline_math(child))
        else:
            text = str(child)
            if text:
                pieces.append(text)
    return re.sub(r"\s+", " ", "".join(pieces)).strip()


def _is_math_tag(tag: Tag) -> bool:
    class_names = " ".join(tag.get("class", []))
    return (
        tag.name == "math"
        or "math" in class_names
        or "tex" in class_names
        or "mathml" in class_names
    )


def _replace_failed_parse_nodes(soup: BeautifulSoup) -> None:
    for text_node in soup.find_all(string=True):
        text = str(text_node)
        if FAILED_TO_PARSE_PREFIX not in text:
            continue

        formula = _extract_failed_parse_formula(text)
        if formula and formula != text:
            text_node.replace_with(soup.new_string(f" {formula} "))


def _replace_math_blocks(soup: BeautifulSoup) -> None:
    for tag in soup.find_all(_is_math_tag):
        replacement = _extract_latex_from_math(tag)
        tag.replace_with(soup.new_string(f" {replacement} "))


def _replace_html_math_blocks(soup: BeautifulSoup) -> None:
    for tag in soup.find_all(class_=lambda classes: classes and ("htmlMath" in classes or "htmlMathText" in classes)):
        rendered = _render_inline_math(tag)
        tag.replace_with(soup.new_string(f" {rendered} "))


def _replace_anchor_tags(soup: BeautifulSoup) -> None:
    for anchor in soup.find_all("a"):
        href = anchor.get("href", "").strip()
        text = anchor.get_text(" ", strip=True)

        if not text and not href:
            anchor.decompose()
            continue

        if href.startswith("#") or href.startswith("javascript:"):
            anchor.replace_with(soup.new_string(f" {text} "))
            continue

        if (
            href.startswith("http://")
            or href.startswith("https://")
            or "doi.org" in href
            or "wikipedia.org" in href
            or "wikimedia.org" in href
        ):
            anchor.decompose()
            continue

        if href.startswith("/"):
            href = href[1:]

        if href and text:
            marker = f'$href="{href}",text="{text}"'
        elif href:
            marker = f'$href="{href}"'
        else:
            marker = text
        anchor.replace_with(soup.new_string(f" {marker} "))


def _drop_unwanted_nodes(soup: BeautifulSoup) -> None:
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    for edit_section in soup.select(".mw-editsection, .mw-editsection-bracket, .mw-editsection-divider"):
        edit_section.decompose()

    for backlink in soup.select(".mw-cite-backlink, .reference, sup.reference, li[id^='cite_note']"):
        backlink.decompose()

    for tag in soup.find_all(list(BLOCK_TAGS)):
        tag.decompose()


def _normalize_text(text: str) -> str:
    text = _extract_failed_parse_formula(text)
    text = re.sub(r"\[[^\]]*\]", " ", text)
    text = re.sub(r"\b↑\b", " ", text)
    return replace_symbols(re.sub(r"\s+", " ", text).strip())


def clean_html_for_llm(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    _drop_unwanted_nodes(soup)
    _replace_math_blocks(soup)
    _replace_html_math_blocks(soup)
    _replace_anchor_tags(soup)
    _replace_failed_parse_nodes(soup)

    main = soup.find(id="mw-content-text") or soup.body or soup
    for heading in main.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        heading_text = heading.get_text(" ", strip=True).lower()
        if heading_text == "references":
            for sibling in list(heading.find_all_next()):
                sibling.decompose()
            heading.decompose()
            break

    for tag in main.find_all(["sup", "sub"]):
        tag.insert_before(" ")
        tag.insert_after(" ")

    for tag in main.find_all("pre"):
        code_text = tag.get_text(" ", strip=True)
        tag.replace_with(soup.new_string(f" {code_text} "))

    text = main.get_text(separator=" ", strip=True)
    return replace_symbols(_normalize_text(text))


def html_to_clean_text(html_path: str | Path) -> str:
    path = Path(html_path)
    return clean_html_for_llm(path.read_text(encoding="utf-8"))


def html_to_txt_file(html_path: str | Path, output_path: str | Path) -> Path:
    source = Path(html_path)
    target = Path(output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(clean_html_for_llm(source.read_text(encoding="utf-8")), encoding="utf-8")
    return target
