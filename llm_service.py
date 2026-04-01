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
        "Do not include definitions, explanations, or markdown. "
        "Use only concepts that appear in the provided text. "
        "If a concept already exists in the graph, reuse its exact title. "
        "If it is new, keep the title concise and stable. "
        "Dependencies must reference concept titles needed to understand the concept. "
        "Keep concept titles deterministic across pages. "
        "When a concept already exists in the context summary, preserve its dependency intent and only add missing dependencies inferred from the current pages.\n\n"
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
