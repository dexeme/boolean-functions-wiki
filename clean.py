from __future__ import annotations

import json
from pathlib import Path

JSON_DIR = Path("jsons")
PAGES_PATH = JSON_DIR / "pages.json"
CONCEPTS_PATH = JSON_DIR / "concepts.json"
DEPENDENCY_GRAPH_PATH = JSON_DIR / "dependency_graph.json"
DEPENDENCY_DOT_PATH = JSON_DIR / "dependency_graph.dot"


def ensure_json_dir() -> None:
    JSON_DIR.mkdir(parents=True, exist_ok=True)


def reset_json_files() -> None:
    ensure_json_dir()
    PAGES_PATH.write_text(json.dumps({"pages": []}, indent=2, ensure_ascii=False), encoding="utf-8")
    CONCEPTS_PATH.write_text(json.dumps({"concepts": {}}, indent=2, ensure_ascii=False), encoding="utf-8")
    DEPENDENCY_GRAPH_PATH.write_text(
        json.dumps(
            {
                "nodes": [],
                "edges": [],
                "dependencies_by_concept": {},
                "dependents_by_concept": {},
                "missing_dependencies": {},
                "has_cycle": False,
                "cycle_nodes": [],
                "topological_order": [],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    DEPENDENCY_DOT_PATH.write_text("digraph Dependencies {\n  rankdir=\"LR\";\n}\n", encoding="utf-8")


def main() -> None:
    reset_json_files()
    print(PAGES_PATH)
    print(CONCEPTS_PATH)
    print(DEPENDENCY_GRAPH_PATH)
    print(DEPENDENCY_DOT_PATH)


if __name__ == "__main__":
    main()
