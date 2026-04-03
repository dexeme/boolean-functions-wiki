from __future__ import annotations

import json
from collections import defaultdict, deque
from pathlib import Path
from typing import TypedDict

JSON_DIR = Path("jsons")
CONCEPTS_PATH = JSON_DIR / "concepts.json"
GRAPH_PATH = JSON_DIR / "dependency_graph.json"
DOT_PATH = JSON_DIR / "dependency_graph.dot"
ROOT_CONCEPT = "Boolean Functions"


class ConceptNode(TypedDict):
    dependencies: list[str]


class ConceptsFile(TypedDict):
    concepts: dict[str, ConceptNode]


class GraphOutput(TypedDict):
    nodes: list[str]
    edges: list[dict[str, str]]
    dependencies_by_concept: dict[str, list[str]]
    dependents_by_concept: dict[str, list[str]]
    missing_dependencies: dict[str, list[str]]
    has_cycle: bool
    cycle_nodes: list[str]
    topological_order: list[str]


def load_concepts(path: Path) -> ConceptsFile:
    if not path.exists():
        raise FileNotFoundError(f"Missing concepts file: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "concepts" not in data or not isinstance(data["concepts"], dict):
        raise ValueError("Invalid concepts format. Expected {'concepts': {name: {'dependencies': [...]}}}.")

    return data


def build_graph(concepts_file: ConceptsFile) -> GraphOutput:
    concepts = concepts_file["concepts"]
    nodes = sorted(concepts.keys())

    dependencies_by_concept: dict[str, list[str]] = {}
    dependents_by_concept: dict[str, list[str]] = defaultdict(list)
    missing_dependencies: dict[str, list[str]] = {}
    edges: list[dict[str, str]] = []

    undirected: dict[str, set[str]] = defaultdict(set)

    for concept in nodes:
        raw_deps = concepts.get(concept, {}).get("dependencies", [])
        deps = sorted({dep for dep in raw_deps if isinstance(dep, str) and dep.strip()})
        dependencies_by_concept[concept] = deps

        missing = [dep for dep in deps if dep not in concepts]
        if missing:
            missing_dependencies[concept] = missing

        for dep in deps:
            edges.append({"from": dep, "to": concept})
            dependents_by_concept[dep].append(concept)
            if dep in concepts:
                undirected[concept].add(dep)
                undirected[dep].add(concept)

    for concept in nodes:
        dependents_by_concept.setdefault(concept, [])
    for concept in dependents_by_concept:
        dependents_by_concept[concept] = sorted(set(dependents_by_concept[concept]))

    for concept in nodes:
        undirected.setdefault(concept, set())

    main_component = connected_component_from_root(undirected, ROOT_CONCEPT)
    if main_component:
        nodes = sorted(node for node in nodes if node in main_component)
        dependencies_by_concept = {
            concept: [dep for dep in deps if dep in main_component]
            for concept, deps in dependencies_by_concept.items()
            if concept in main_component
        }
        dependents_by_concept = {
            concept: [dep for dep in deps if dep in main_component]
            for concept, deps in dependents_by_concept.items()
            if concept in main_component
        }
        edges = [edge for edge in edges if edge["from"] in main_component and edge["to"] in main_component]
        missing_dependencies = {k: v for k, v in missing_dependencies.items() if k in main_component}

    order, cycle_nodes = topological_sort(nodes, dependencies_by_concept)

    return {
        "nodes": nodes,
        "edges": edges,
        "dependencies_by_concept": dependencies_by_concept,
        "dependents_by_concept": dict(dependents_by_concept),
        "missing_dependencies": missing_dependencies,
        "has_cycle": len(cycle_nodes) > 0,
        "cycle_nodes": cycle_nodes,
        "topological_order": order,
    }


def connected_component_from_root(adjacency: dict[str, set[str]], root: str) -> set[str]:
    if root not in adjacency:
        return set()

    visited: set[str] = set()
    queue: deque[str] = deque([root])

    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in adjacency.get(node, set()):
            if neighbor not in visited:
                queue.append(neighbor)

    return visited


def topological_sort(nodes: list[str], deps_by_concept: dict[str, list[str]]) -> tuple[list[str], list[str]]:
    in_degree: dict[str, int] = {node: 0 for node in nodes}
    outgoing: dict[str, list[str]] = defaultdict(list)

    for node in nodes:
        for dep in deps_by_concept.get(node, []):
            if dep not in in_degree:
                continue
            outgoing[dep].append(node)
            in_degree[node] += 1

    queue = deque(sorted(node for node in nodes if in_degree[node] == 0))
    order: list[str] = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in sorted(outgoing.get(node, [])):
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)

    if len(order) == len(nodes):
        return order, []

    cycle_nodes = sorted(node for node, degree in in_degree.items() if degree > 0)
    return order, cycle_nodes


def write_dot(graph: GraphOutput, path: Path) -> None:
    lines = ["digraph Dependencies {"]
    lines.append('  rankdir="LR";')

    for node in graph["nodes"]:
        safe = node.replace('"', '\\"')
        lines.append(f'  "{safe}";')

    for edge in graph["edges"]:
        src = edge["from"].replace('"', '\\"')
        dst = edge["to"].replace('"', '\\"')
        lines.append(f'  "{src}" -> "{dst}";')

    lines.append("}")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    concepts_file = load_concepts(CONCEPTS_PATH)
    graph = build_graph(concepts_file)

    JSON_DIR.mkdir(parents=True, exist_ok=True)
    GRAPH_PATH.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")
    write_dot(graph, DOT_PATH)

    print(f"nodes: {len(graph['nodes'])}")
    print(f"edges: {len(graph['edges'])}")
    print(f"has_cycle: {graph['has_cycle']}")
    print(f"missing_dependencies: {sum(len(v) for v in graph['missing_dependencies'].values())}")
    print(GRAPH_PATH)
    print(DOT_PATH)

if __name__ == "__main__":
    main()
