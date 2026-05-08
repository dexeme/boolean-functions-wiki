PRAGMA foreign_keys = ON;

INSERT OR IGNORE INTO source_pages (
    id,
    slug,
    title,
    url,
    description
)
VALUES (
    1,
    'known_instances_apn_gf_2_7',
    'Known instances of APN functions over GF(2^7)',
    NULL,
    'Source page listing known APN functions over GF(2^7).'
);

INSERT OR IGNORE INTO source_tables (
    id,
    page_id,
    slug,
    title,
    table_kind,
    description
)
VALUES (
    1,
    1,
    'known_apn_functions',
    'Known APN functions over GF(2^7)',
    'function_list',
    'Main table containing local source IDs and APN function formulas.'
);

DELETE FROM function_expressions WHERE 1 = 1;
DELETE FROM source_row_function_links WHERE 1 = 1;
DELETE FROM source_external_ids WHERE 1 = 1;
DELETE FROM source_rows WHERE source_table_id = 1;
DELETE FROM apn_functions WHERE dimension = 7 AND field_label = 'GF(2^7)';