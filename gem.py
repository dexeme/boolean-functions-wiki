import json
import os
import sys

import google.generativeai as genai
from bs4 import BeautifulSoup

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=api_key)

DATA_DIR = "data"
JSON_DIR = "jsons"
CONCEPTS_PATH = os.path.join(JSON_DIR, "concepts.json")
PAGES_PATH = os.path.join(JSON_DIR, "pages.json")
TARGET_FILE = os.path.join(DATA_DIR, "Algebraic immunity of Boolean functions.html")
ROOT_TITLE = "Boolean Functions"


def clean_html_for_llm(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside", "form"]):
        tag.decompose()

    content_div = soup.find(id="mw-content-text") or soup.body or soup
    text = content_div.get_text(separator="\n", strip=True)
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def parse_and_format_json(json_text):
    data = json.loads(json_text)
    return data, json.dumps(data, indent=2, ensure_ascii=False)


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(JSON_DIR, exist_ok=True)


def load_json_file(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def list_html_files():
    if not os.path.isdir(DATA_DIR):
        return []
    return sorted(
        os.path.join(DATA_DIR, name)
        for name in os.listdir(DATA_DIR)
        if name.endswith(".html")
    )


def parse_range_argument(value, total_files):
    if not value:
        return 0, total_files

    if "-" not in value:
        index = int(value) - 1
        return index, index + 1

    start_text, end_text = value.split("-", 1)
    start = int(start_text) - 1 if start_text else 0
    end = int(end_text) if end_text else total_files
    return max(start, 0), min(end, total_files)


def initialize_state():
    graph = load_json_file(CONCEPTS_PATH, {"concepts": []})
    page_index = load_json_file(PAGES_PATH, {"pages": []})

    if not isinstance(graph, dict):
        graph = {"concepts": []}
    if "concepts" not in graph or not isinstance(graph["concepts"], list):
        graph["concepts"] = []

    if not isinstance(page_index, dict):
        page_index = {"pages": []}
    if "pages" not in page_index or not isinstance(page_index["pages"], list):
        page_index["pages"] = []

    if not any(concept.get("title") == ROOT_TITLE for concept in graph["concepts"]):
        graph["concepts"].append(
            {
                "uid": 1,
                "title": ROOT_TITLE,
                "dependencies": [],
            }
        )

    return graph, page_index


def build_title_to_uid_map(graph):
    return {concept["title"]: concept["uid"] for concept in graph["concepts"]}


def next_uid(graph):
    if not graph["concepts"]:
        return 1
    return max(concept["uid"] for concept in graph["concepts"]) + 1


def get_page_uid(page):
    return page.get("uid", page.get("page_uid", 0))


def build_pages_index(html_files):
    pages = []
    for index, filepath in enumerate(html_files, start=1):
        pages.append(
            {
                "uid": index,
                "title": os.path.splitext(os.path.basename(filepath))[0],
                "source_file": os.path.basename(filepath),
                "concepts": [],
            }
        )
    return {"pages": pages}


def build_context_summary(graph):
    concepts = [
        {"uid": concept["uid"], "title": concept["title"]}
        for concept in graph["concepts"]
    ]
    return json.dumps({"concepts": concepts}, ensure_ascii=False)


def build_page_payload(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        html_content = f.read()

    clean_text = clean_html_for_llm(html_content)
    page_title = os.path.splitext(os.path.basename(filepath))[0]

    return {
        "title": page_title,
        "source_file": os.path.basename(filepath),
        "text": clean_text[:30000],
    }


def process_pages_batch(page_index, graph, batch_payload):
    title_to_uid = build_title_to_uid_map(graph)

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = (
        f"Existing knowledge graph summary:\n{build_context_summary(graph)}\n\n"
        "Map the page content to this knowledge graph. "
        "Return only JSON matching the schema. "
        "Do not include definitions, explanations, or markdown. "
        "Use only concepts that appear in the page text. "
        "If a concept already exists in the graph, reuse its exact title. "
        "If it is new, keep the title concise and stable. "
        "Dependencies must reference concept titles needed to understand the concept.\n\n"
        f"Pages to process:\n{json.dumps(batch_payload, ensure_ascii=False)}"
    )

    generation_config = {
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "object",
            "properties": {
                "pages": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "uid": {"type": "integer", "description": "Page UID"},
                            "concepts": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "t": {"type": "string", "description": "Concept title"},
                                        "dep": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": "Concept titles required to understand this concept"
                                        }
                                    },
                                    "required": ["t", "dep"]
                                }
                            }
                        },
                        "required": ["uid", "concepts"]
                    }
                }
            },
            "required": ["pages"]
        }
    }

    response = model.generate_content(prompt, generation_config=generation_config)
    response_data, formatted_json = parse_and_format_json(response.text)

    page_lookup = {page["uid"]: page for page in page_index["pages"]}
    for page_data in response_data.get("pages", []):
        page_uid = page_data.get("uid")
        if page_uid not in page_lookup:
            continue

        resolved_concepts = []
        for item in page_data.get("concepts", []):
            concept_title = item["t"].strip()
            if not concept_title:
                continue

            concept_uid = title_to_uid.get(concept_title)
            if concept_uid is None:
                concept_uid = next_uid(graph)
                graph["concepts"].append(
                    {
                        "uid": concept_uid,
                        "title": concept_title,
                        "dependencies": [],
                    }
                )
                title_to_uid[concept_title] = concept_uid

            dependency_uids = []
            for dep_title in item.get("dep", []):
                dep_title = dep_title.strip()
                if not dep_title:
                    continue
                dep_uid = title_to_uid.get(dep_title)
                if dep_uid is None:
                    dep_uid = next_uid(graph)
                    graph["concepts"].append(
                        {
                            "uid": dep_uid,
                            "title": dep_title,
                            "dependencies": [],
                        }
                    )
                    title_to_uid[dep_title] = dep_uid
                if dep_uid not in dependency_uids:
                    dependency_uids.append(dep_uid)

            for concept in graph["concepts"]:
                if concept["uid"] == concept_uid:
                    concept["dependencies"] = sorted(set(concept.get("dependencies", []) + dependency_uids))
                    break

            resolved_concepts.append(concept_uid)

        page_lookup[page_uid]["concepts"] = resolved_concepts

    ensure_data_dir()
    save_json_file(CONCEPTS_PATH, graph)
    save_json_file(PAGES_PATH, page_index)

    return formatted_json


if __name__ == "__main__":
    graph_state, page_state = initialize_state()
    html_files = list_html_files()
    range_arg = sys.argv[1] if len(sys.argv) > 1 else ""
    start, end = parse_range_argument(range_arg, len(html_files))
    selected_files = html_files[start:end]

    page_state = build_pages_index(selected_files)
    ensure_data_dir()
    save_json_file(PAGES_PATH, page_state)

    batch_payload = [build_page_payload(filepath) for filepath in selected_files]

    print(f"Processing {len(selected_files)} pages in one Gemini request...")
    output = process_pages_batch(page_state, graph_state, batch_payload)
    print(output)
