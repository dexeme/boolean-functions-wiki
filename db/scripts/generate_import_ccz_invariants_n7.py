#!/usr/bin/env python3
"""Generate SQL to import CCZ invariant tables for APN functions in dimension 7."""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "docs" / "content" / "tables"
OUTPUT_PATH = ROOT / "db" / "generated" / "import_ccz_invariants_n7.sql"

SOURCE_PAGE = {
    "slug": "ccz_invariants_apn_functions_dimension_7",
    "title": "CCZ invariants for all known APN functions in dimension 7",
    "url": None,
    "description": "Source page listing CCZ invariants for all known APN functions in dimension 7.",
}

REFERENCED_FUNCTION_TABLE_SLUG = "known_apn_functions"


@dataclass(frozen=True)
class InvariantTable:
    csv_name: str
    table_slug: str
    table_title: str
    invariant_slug: str
    invariant_label: str
    dedicated_table: str
    dedicated_value_column: str
    source_table_description: str


@dataclass(frozen=True)
class SqlExpression:
    value: str


INVARIANT_TABLES = [
    InvariantTable(
        csv_name="CCZ-invariants_for_all_known_APN_functions_in_dimension_7_table_01.csv",
        table_slug="ccz_invariants_dimension_7_gamma_rank",
        table_title="CCZ invariants for APN functions in dimension 7: Gamma-rank",
        invariant_slug="gamma-rank",
        invariant_label="Gamma-rank",
        dedicated_table="function_gamma_ranks",
        dedicated_value_column="gamma_rank",
        source_table_description="Gamma-rank values and referenced APN function indices.",
    ),
    InvariantTable(
        csv_name="CCZ-invariants_for_all_known_APN_functions_in_dimension_7_table_02.csv",
        table_slug="ccz_invariants_dimension_7_delta_rank",
        table_title="CCZ invariants for APN functions in dimension 7: Delta-rank",
        invariant_slug="delta-rank",
        invariant_label="Delta-rank",
        dedicated_table="function_delta_ranks",
        dedicated_value_column="delta_rank",
        source_table_description="Delta-rank values and referenced APN function indices.",
    ),
    InvariantTable(
        csv_name="CCZ-invariants_for_all_known_APN_functions_in_dimension_7_table_03.csv",
        table_slug="ccz_invariants_dimension_7_multiplier_group_order",
        table_title="CCZ invariants for APN functions in dimension 7: Multiplier group order",
        invariant_slug="multiplier-group-order",
        invariant_label="Multiplier group order",
        dedicated_table="function_multiplier_group_orders",
        dedicated_value_column="multiplier_group_order",
        source_table_description="Multiplier group order values and referenced APN function indices.",
    ),
]


def sql_literal(value: object) -> str:
    if isinstance(value, SqlExpression):
        return value.value
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"


def clean_cell(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == "`" and value[-1] == "`":
        value = value[1:-1]
    return value.strip()


def parse_indices(raw_indices: str, warnings: list[str], csv_name: str, row_number: int) -> list[str]:
    indices: list[str] = []
    for token in clean_cell(raw_indices).split(","):
        token = token.strip()
        if not token:
            continue
        if re.fullmatch(r"\d+", token):
            indices.append(str(int(token)))
            continue

        leading_integer = re.match(r"^(\d+)\b", token)
        if leading_integer:
            index = str(int(leading_integer.group(1)))
            indices.append(index)
            warnings.append(
                f"{csv_name}: row {row_number} has non-canonical index token "
                f"{token!r}; imported only leading index {index!r}."
            )
            continue

        warnings.append(f"{csv_name}: row {row_number} ignored non-numeric index token {token!r}.")
    return indices


def read_rows(table: InvariantTable, warnings: list[str]) -> list[dict[str, object]]:
    path = TABLE_DIR / table.csv_name
    rows: list[dict[str, object]] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        if fieldnames != [table.invariant_label, "Indices"]:
            raise ValueError(f"{path} has unexpected header {fieldnames!r}")
        for row_number, row in enumerate(reader, start=1):
            value_text = clean_cell(row[table.invariant_label])
            raw_indices = row["Indices"]
            indices = parse_indices(raw_indices, warnings, table.csv_name, row_number)
            rows.append(
                {
                    "row_number": row_number,
                    "value_text": value_text,
                    "raw_indices": raw_indices,
                    "indices": indices,
                    "raw_json": json.dumps(
                        {
                            table.invariant_label: row[table.invariant_label],
                            "Indices": raw_indices,
                        },
                        ensure_ascii=True,
                        separators=(",", ":"),
                    ),
                }
            )
    return rows


def append_values_insert(lines: list[str], table_name: str, columns: list[str], rows: list[list[object]]) -> None:
    if not rows:
        return
    lines.append(f"INSERT OR IGNORE INTO {table_name} (")
    lines.append("    " + ",\n    ".join(columns))
    lines.append(")")
    lines.append("VALUES")
    for index, row in enumerate(rows):
        suffix = "," if index < len(rows) - 1 else ";"
        lines.append("    (" + ", ".join(sql_literal(value) for value in row) + ")" + suffix)
    lines.append("")


def generate_sql() -> str:
    warnings: list[str] = []
    imported_rows = {table: read_rows(table, warnings) for table in INVARIANT_TABLES}

    lines: list[str] = [
        "-- Generated by db/generate_import_ccz_invariants_n7.py.",
        "-- Imports the three CCZ invariant CSV tables for known APN functions in dimension 7.",
    ]
    for warning in warnings:
        lines.append(f"-- WARNING: {warning}")
    lines.extend(["", "PRAGMA foreign_keys = ON;", "BEGIN;", ""])

    append_values_insert(
        lines,
        "source_pages",
        ["slug", "title", "url", "description"],
        [[SOURCE_PAGE["slug"], SOURCE_PAGE["title"], SOURCE_PAGE["url"], SOURCE_PAGE["description"]]],
    )

    append_values_insert(
        lines,
        "invariant_types",
        ["slug", "label", "value_kind", "description"],
        [
            [
                table.invariant_slug,
                table.invariant_label,
                "integer",
                f"{table.invariant_label} imported from CCZ invariants for dimension 7.",
            ]
            for table in INVARIANT_TABLES
        ],
    )

    for table in INVARIANT_TABLES:
        lines.extend(
            [
                "INSERT OR IGNORE INTO source_tables (",
                "    page_id,",
                "    slug,",
                "    title,",
                "    table_kind,",
                "    description",
                ")",
                "SELECT",
                "    p.id,",
                f"    {sql_literal(table.table_slug)},",
                f"    {sql_literal(table.table_title)},",
                "    'invariant_table',",
                f"    {sql_literal(table.source_table_description)}",
                "FROM source_pages p",
                f"WHERE p.slug = {sql_literal(SOURCE_PAGE['slug'])};",
                "",
            ]
        )

    table_slugs = ", ".join(sql_literal(table.table_slug) for table in INVARIANT_TABLES)
    lines.extend(
        [
            "-- Refresh only the source rows from these invariant tables; dependent",
            "-- source_references and function_invariants are removed by ON DELETE CASCADE.",
            "DELETE FROM source_rows",
            "WHERE source_table_id IN (",
            "    SELECT id FROM source_tables",
            f"    WHERE slug IN ({table_slugs})",
            ");",
            "",
        ]
    )

    for table in INVARIANT_TABLES:
        rows = imported_rows[table]
        staging_rows = []
        for row in rows:
            for external_id in row["indices"]:
                staging_rows.append(
                    [
                        table.table_slug,
                        table.invariant_slug,
                        table.csv_name,
                        row["row_number"],
                        row["value_text"],
                        int(row["value_text"]),
                        row["raw_indices"],
                        row["raw_json"],
                        external_id,
                    ]
                )

        lines.extend(
            [
                "DROP TABLE IF EXISTS imported_ccz_invariants_n7;",
                "CREATE TEMP TABLE imported_ccz_invariants_n7 (",
                "    table_slug TEXT NOT NULL,",
                "    invariant_slug TEXT NOT NULL,",
                "    csv_name TEXT NOT NULL,",
                "    row_number INTEGER NOT NULL,",
                "    value_text TEXT NOT NULL,",
                "    numeric_value INTEGER NOT NULL,",
                "    raw_indices TEXT NOT NULL,",
                "    raw_json TEXT NOT NULL,",
                "    external_id TEXT NOT NULL",
                ");",
                "",
            ]
        )
        append_values_insert(
            lines,
            "imported_ccz_invariants_n7",
            [
                "table_slug",
                "invariant_slug",
                "csv_name",
                "row_number",
                "value_text",
                "numeric_value",
                "raw_indices",
                "raw_json",
                "external_id",
            ],
            staging_rows,
        )

        lines.extend(
            [
                "INSERT INTO source_rows (",
                "    source_table_id,",
                "    row_number,",
                "    raw_label,",
                "    raw_value,",
                "    raw_json",
                ")",
                "SELECT DISTINCT",
                "    source_table.id,",
                "    imported.row_number,",
                "    imported.value_text,",
                "    imported.raw_indices,",
                "    imported.raw_json",
                "FROM imported_ccz_invariants_n7 imported",
                "JOIN source_tables source_table ON source_table.slug = imported.table_slug;",
                "",
                "INSERT INTO source_references (",
                "    source_row_id,",
                "    referenced_source_table_id,",
                "    id_kind,",
                "    external_id,",
                "    function_id,",
                "    resolution_note",
                ")",
                "SELECT",
                "    source_row.id,",
                "    referenced_table.id,",
                "    'wiki_id',",
                "    imported.external_id,",
                "    linked.function_id,",
                "    'Resolved from Indices cell in ' || imported.csv_name",
                "FROM imported_ccz_invariants_n7 imported",
                "JOIN source_tables source_table ON source_table.slug = imported.table_slug",
                "JOIN source_rows source_row",
                "    ON source_row.source_table_id = source_table.id",
                "   AND source_row.row_number = imported.row_number",
                "JOIN source_tables referenced_table",
                f"    ON referenced_table.slug = {sql_literal(REFERENCED_FUNCTION_TABLE_SLUG)}",
                "JOIN source_external_ids external_id",
                "    ON external_id.id_kind = 'wiki_id'",
                "   AND external_id.external_id = imported.external_id",
                "JOIN source_row_function_links linked",
                "    ON linked.source_row_id = external_id.source_row_id;",
                "",
                "INSERT INTO function_invariants (",
                "    function_id,",
                "    invariant_type_id,",
                "    value_text,",
                "    numeric_value,",
                "    source_row_id,",
                "    source_reference_id,",
                "    notes",
                ")",
                "SELECT",
                "    reference.function_id,",
                "    invariant_type.id,",
                "    imported.value_text,",
                "    imported.numeric_value,",
                "    source_row.id,",
                "    reference.id,",
                "    'Imported from ' || imported.csv_name",
                "FROM imported_ccz_invariants_n7 imported",
                "JOIN source_tables source_table ON source_table.slug = imported.table_slug",
                "JOIN source_rows source_row",
                "    ON source_row.source_table_id = source_table.id",
                "   AND source_row.row_number = imported.row_number",
                "JOIN invariant_types invariant_type ON invariant_type.slug = imported.invariant_slug",
                "JOIN source_references reference",
                "    ON reference.source_row_id = source_row.id",
                "   AND reference.id_kind = 'wiki_id'",
                "   AND reference.external_id = imported.external_id;",
                "",
                f"INSERT INTO {table.dedicated_table} (",
                "    function_id,",
                f"    {table.dedicated_value_column},",
                "    value_text,",
                "    source_row_id,",
                "    source_reference_id,",
                "    notes",
                ")",
                "SELECT",
                "    reference.function_id,",
                "    imported.numeric_value,",
                "    imported.value_text,",
                "    source_row.id,",
                "    reference.id,",
                "    'Imported from ' || imported.csv_name",
                "FROM imported_ccz_invariants_n7 imported",
                "JOIN source_tables source_table ON source_table.slug = imported.table_slug",
                "JOIN source_rows source_row",
                "    ON source_row.source_table_id = source_table.id",
                "   AND source_row.row_number = imported.row_number",
                "JOIN source_references reference",
                "    ON reference.source_row_id = source_row.id",
                "   AND reference.id_kind = 'wiki_id'",
                "   AND reference.external_id = imported.external_id;",
                "",
            ]
        )

    lines.extend(["COMMIT;", ""])
    return "\n".join(lines)


def main() -> None:
    OUTPUT_PATH.write_text(generate_sql(), encoding="utf-8")
    print(OUTPUT_PATH.relative_to(ROOT))


if __name__ == "__main__":
    main()
