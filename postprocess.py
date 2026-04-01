from __future__ import annotations

import json
from typing import Any, TypedDict


class ConceptRecord(TypedDict):
    dependencies: list[str]


class PageRecord(TypedDict):
    title: str
    url: str
    concepts: list[str]


class ConceptsFile(TypedDict):
    concepts: dict[str, ConceptRecord]


class PagesFile(TypedDict):
    pages: list[PageRecord]


class GeminiConcept(TypedDict):
    t: str
    dep: list[str]


class GeminiPage(TypedDict):
    title: str
    concepts: list[GeminiConcept]


class GeminiBatchResponse(TypedDict):
    pages: list[GeminiPage]


def parse_and_format_json(json_text: str) -> tuple[GeminiBatchResponse, str]:
    data: GeminiBatchResponse = json.loads(json_text)
    return data, json.dumps(data, indent=2, ensure_ascii=False)


def merge_gemini_output(
    graph: ConceptsFile,
    page_index: PagesFile,
    response_data: GeminiBatchResponse,
) -> None:
    concepts_map: dict[str, ConceptRecord] = graph["concepts"]
    page_lookup: dict[str, PageRecord] = {page["title"]: page for page in page_index["pages"]}

    for page_data in response_data.get("pages", []):
        page_title: str = page_data.get("title", "").strip()
        if not page_title or page_title not in page_lookup:
            continue

        resolved_concepts: list[str] = []
        for item in page_data.get("concepts", []):
            concept_title: str = item["t"].strip()
            if not concept_title:
                continue

            if concept_title not in concepts_map:
                concepts_map[concept_title] = {"dependencies": []}

            dependency_titles: list[str] = []
            for dep_title in item.get("dep", []):
                dep_title = dep_title.strip()
                if not dep_title:
                    continue
                if dep_title not in concepts_map:
                    concepts_map[dep_title] = {"dependencies": []}
                if dep_title not in dependency_titles:
                    dependency_titles.append(dep_title)

            concepts_map[concept_title]["dependencies"] = sorted(
                set(concepts_map[concept_title].get("dependencies", []) + dependency_titles)
            )
            resolved_concepts.append(concept_title)

        page_lookup[page_title]["concepts"] = resolved_concepts
