PRAGMA foreign_keys = ON;

CREATE TEMP TABLE imported_apn_functions_n7 (
    source_id TEXT,
    formula_latex TEXT
);

.mode csv
.import --skip 1 docs/content/tables/known_instances_apn_gf2_7.csv imported_apn_functions_n7

INSERT INTO apn_functions (
    stable_id,
    dimension,
    field_label,
    formula_latex,
    formula_normalized,
    notes
)
SELECT
    'apn-gf-2-7-' || printf('%04d', CAST(source_id AS INTEGER)),
    7,
    'GF(2^7)',
    replace(replace(formula_latex, '`', ''), '$', ''),
    lower(replace(replace(replace(formula_latex, '`', ''), '$', ''), ' ', '')),
    'Imported from Known instances of APN functions over GF(2^7).'
FROM imported_apn_functions_n7;

INSERT INTO source_rows (
    source_table_id,
    row_number,
    raw_label,
    raw_value,
    raw_json
)
SELECT
    1,
    CAST(source_id AS INTEGER),
    source_id,
    formula_latex,
    json_object('ID', source_id, 'F(x)', formula_latex)
FROM imported_apn_functions_n7;

INSERT INTO source_external_ids (
    source_row_id,
    id_kind,
    external_id
)
SELECT
    r.id,
    'wiki_id',
    i.source_id
FROM imported_apn_functions_n7 i
JOIN source_rows r
    ON r.source_table_id = 1
   AND r.raw_label = i.source_id;

INSERT INTO source_row_function_links (
    source_row_id,
    function_id,
    link_role,
    confidence,
    notes
)
SELECT
    r.id,
    f.id,
    'defined_by',
    'imported',
    'Imported from the known APN functions table.'
FROM imported_apn_functions_n7 i
JOIN source_rows r
    ON r.source_table_id = 1
   AND r.raw_label = i.source_id
JOIN apn_functions f
    ON f.stable_id = 'apn-gf-2-7-' || printf('%04d', CAST(i.source_id AS INTEGER));

INSERT INTO function_expressions (
    function_id,
    expression_kind,
    expression_latex,
    expression_normalized,
    source_row_id,
    confidence,
    notes
)
SELECT
    f.id,
    'polynomial',
    f.formula_latex,
    f.formula_normalized,
    r.id,
    'imported',
    'Imported from the known APN functions table.'
FROM imported_apn_functions_n7 i
JOIN apn_functions f
    ON f.stable_id = 'apn-gf-2-7-' || printf('%04d', CAST(i.source_id AS INTEGER))
JOIN source_rows r
    ON r.source_table_id = 1
   AND r.raw_label = i.source_id;