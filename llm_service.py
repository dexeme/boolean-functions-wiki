from __future__ import annotations

import json
from typing import Any, TypedDict

import google.generativeai as genai


class PagePayload(TypedDict):
    href: str
    url: str
    title: str
    source_file: str
    text: str


class GeminiConcept(TypedDict):
    t: str
    dep: list[str]


class GeminiPage(TypedDict):
    title: str
    concepts: list[GeminiConcept]


class GeminiBatchResponse(TypedDict):
    pages: list[GeminiPage]


def build_context_summary(concepts: dict[str, dict[str, list[str]]]) -> str:
    summary: dict[str, list[dict[str, Any]]] = {
        "concepts_with_dependencies": [
            {"title": title, "dependencies": data.get("dependencies", [])}
            for title, data in concepts.items()
        ]
    }
    return json.dumps(summary, ensure_ascii=False)


def build_generation_config() -> dict[str, Any]:
    return {
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "object",
            "properties": {
                "pages": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Page title"},
                            "concepts": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "t": {"type": "string", "description": "Concept title"},
                                        "dep": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "Concept titles required to understand this concept",
                                        },
                                    },
                                    "required": ["t", "dep"],
                                },
                            },
                        },
                        "required": ["title", "concepts"],
                    },
                }
            },
            "required": ["pages"],
        },
    }


def build_prompt(graph_concepts: dict[str, dict[str, list[str]]], batch_payload: list[PagePayload]) -> str:
    context_summary = build_context_summary(graph_concepts)
    payload_text = json.dumps(batch_payload, ensure_ascii=False)
    return (
        f"Existing knowledge graph summary:\n{context_summary}\n\n"
        "Each page payload already contains cleaned plain text extracted from wiki HTML. "
        "Fields: href (canonical wiki slug), url (full page url), title, source_file, text. "
        "Map each page's cleaned text to the knowledge graph. "
        "Return only JSON matching the schema. "
        "Do not include definitions, explanations, or markdown.\n\n"

        "Concept extraction rules:\n"
        "- Use only concepts that appear in the provided text.\n"
        "- If a concept already exists in the graph, reuse its exact title.\n"
        "- If it is new, keep the title concise, stable, and deterministic.\n"
        "- Detect synonyms, spelling variants, singular/plural, capitalization variants and normalize to one canonical title.\n"
        "- Prefer core domain concepts that are structurally useful across pages.\n"
        "- Ignore topics that appear only as side notes, trivia, historical curiosities, or one-off mentions.\n"
        "- Avoid creating nodes for page-local examples or temporary notation.\n\n"

        "Dependency rules:\n"
        "- A dependency edge A -> B means: understanding A is required to understand B.\n"
        "- Only create dependencies when the text indicates:\n"
        "  * B is defined using A\n"
        "  * B is derived from A\n"
        "  * B is computed or measured using A\n"
        "  * B explicitly builds on A\n"
        "- Do NOT create dependencies when A is only:\n"
        "  * an example of B\n"
        "  * a subtype or family of B\n"
        "  * a construction producing B\n"
        "  * an application of B\n"
        "  * historically related to B\n"
        "  * mentioned in the same paragraph without conceptual dependence\n"
        "  * more general or more specific than B without explicit prerequisite relationship\n"
        "  * equivalent to B only under certain conditions\n"
        "  * commonly compared in literature without conceptual dependency\n\n"

        "Direction rules:\n"
        "- If B is defined using A, emit A -> B\n"
        "- If B is derived from A, emit A -> B\n"
        "- If a table/transform/representation produces a parameter, emit source -> parameter\n"
        "- If a concept is a table, spectrum, transform, representation, or derivative-based object from which a parameter is computed, emit object -> parameter\n"
        "- Prefer representation-specific parents when available (e.g., Vectorial Boolean Functions -> Univariate representation instead of Boolean Functions -> Univariate representation)\n"
        "- Prefer direct dependencies only, avoid transitive edges\n"
        "- If direction is unclear, do not create the dependency\n\n"

        "Graph quality rules:\n"
        "- Prefer fewer, high-confidence dependencies\n"
        "- Avoid speculative or inferred edges\n"
        "- Avoid cycles unless strongly justified\n"
        "- Avoid duplicate edges\n"
        "- Keep concept titles deterministic across pages\n"
        "- When a concept already exists, preserve previous dependencies and only add missing ones\n"
        "- Prefer under-linking rather than over-linking\n\n"

        f"Pages to process:\n{payload_text}"
    )


def request_batch(
    model_name: str,
    graph_concepts: dict[str, dict[str, list[str]]],
    batch_payload: list[PagePayload],
) -> str:
    model = genai.GenerativeModel(model_name)
    prompt = build_prompt(graph_concepts, batch_payload)
    generation_config = build_generation_config()
    response = model.generate_content(prompt, generation_config=generation_config)
    return response.text
