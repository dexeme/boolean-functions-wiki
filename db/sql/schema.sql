PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS source_pages (
    id INTEGER PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    url TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS source_tables (
    id INTEGER PRIMARY KEY,
    page_id INTEGER NOT NULL REFERENCES source_pages(id) ON DELETE CASCADE,
    slug TEXT NOT NULL,
    title TEXT NOT NULL,
    table_kind TEXT NOT NULL,
    description TEXT,
    UNIQUE (page_id, slug)
);

CREATE TABLE IF NOT EXISTS source_rows (
    id INTEGER PRIMARY KEY,
    source_table_id INTEGER NOT NULL REFERENCES source_tables(id) ON DELETE CASCADE,
    row_number INTEGER NOT NULL,
    raw_label TEXT,
    raw_value TEXT,
    raw_json TEXT,
    UNIQUE (source_table_id, row_number)
);

CREATE TABLE IF NOT EXISTS apn_functions (
    id INTEGER PRIMARY KEY,
    stable_id TEXT NOT NULL UNIQUE,
    dimension INTEGER NOT NULL,
    field_label TEXT NOT NULL,
    formula_latex TEXT NOT NULL,
    formula_normalized TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS source_external_ids (
    id INTEGER PRIMARY KEY,
    source_row_id INTEGER NOT NULL REFERENCES source_rows(id) ON DELETE CASCADE,
    id_kind TEXT NOT NULL DEFAULT 'wiki_id',
    external_id TEXT NOT NULL,
    UNIQUE (source_row_id, id_kind, external_id)
);

CREATE INDEX IF NOT EXISTS idx_source_external_ids_lookup
ON source_external_ids(id_kind, external_id);

CREATE TABLE IF NOT EXISTS source_row_function_links (
    id INTEGER PRIMARY KEY,
    source_row_id INTEGER NOT NULL REFERENCES source_rows(id) ON DELETE CASCADE,
    function_id INTEGER NOT NULL REFERENCES apn_functions(id) ON DELETE CASCADE,
    link_role TEXT NOT NULL DEFAULT 'defined_by',
    confidence TEXT NOT NULL DEFAULT 'seeded',
    notes TEXT,
    UNIQUE (source_row_id, function_id, link_role)
);

CREATE TABLE IF NOT EXISTS invariant_types (
    id INTEGER PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    label TEXT NOT NULL,
    value_kind TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS source_references (
    id INTEGER PRIMARY KEY,
    source_row_id INTEGER NOT NULL REFERENCES source_rows(id) ON DELETE CASCADE,
    referenced_source_table_id INTEGER NOT NULL REFERENCES source_tables(id) ON DELETE CASCADE,
    id_kind TEXT NOT NULL DEFAULT 'wiki_id',
    external_id TEXT NOT NULL,
    function_id INTEGER REFERENCES apn_functions(id) ON DELETE SET NULL,
    resolution_note TEXT
);

CREATE INDEX IF NOT EXISTS idx_source_references_lookup
ON source_references(referenced_source_table_id, id_kind, external_id);

CREATE TABLE IF NOT EXISTS function_invariants (
    id INTEGER PRIMARY KEY,
    function_id INTEGER NOT NULL REFERENCES apn_functions(id) ON DELETE CASCADE,
    invariant_type_id INTEGER NOT NULL REFERENCES invariant_types(id) ON DELETE CASCADE,
    value_text TEXT NOT NULL,
    numeric_value INTEGER,
    source_row_id INTEGER NOT NULL REFERENCES source_rows(id) ON DELETE CASCADE,
    source_reference_id INTEGER REFERENCES source_references(id) ON DELETE SET NULL,
    notes TEXT,
    UNIQUE (function_id, invariant_type_id, value_text, source_row_id)
);

CREATE TABLE IF NOT EXISTS function_gamma_ranks (
    id INTEGER PRIMARY KEY,
    function_id INTEGER NOT NULL UNIQUE REFERENCES apn_functions(id) ON DELETE CASCADE,
    gamma_rank INTEGER NOT NULL,
    value_text TEXT NOT NULL,
    source_row_id INTEGER NOT NULL REFERENCES source_rows(id) ON DELETE CASCADE,
    source_reference_id INTEGER REFERENCES source_references(id) ON DELETE SET NULL,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_function_gamma_ranks_value
ON function_gamma_ranks(gamma_rank);

CREATE TABLE IF NOT EXISTS function_delta_ranks (
    id INTEGER PRIMARY KEY,
    function_id INTEGER NOT NULL UNIQUE REFERENCES apn_functions(id) ON DELETE CASCADE,
    delta_rank INTEGER NOT NULL,
    value_text TEXT NOT NULL,
    source_row_id INTEGER NOT NULL REFERENCES source_rows(id) ON DELETE CASCADE,
    source_reference_id INTEGER REFERENCES source_references(id) ON DELETE SET NULL,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_function_delta_ranks_value
ON function_delta_ranks(delta_rank);

CREATE TABLE IF NOT EXISTS function_multiplier_group_orders (
    id INTEGER PRIMARY KEY,
    function_id INTEGER NOT NULL UNIQUE REFERENCES apn_functions(id) ON DELETE CASCADE,
    multiplier_group_order INTEGER NOT NULL,
    value_text TEXT NOT NULL,
    source_row_id INTEGER NOT NULL REFERENCES source_rows(id) ON DELETE CASCADE,
    source_reference_id INTEGER REFERENCES source_references(id) ON DELETE SET NULL,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_function_multiplier_group_orders_value
ON function_multiplier_group_orders(multiplier_group_order);

CREATE TABLE IF NOT EXISTS function_expressions (
    id INTEGER PRIMARY KEY,
    function_id INTEGER NOT NULL REFERENCES apn_functions(id) ON DELETE CASCADE,
    expression_kind TEXT NOT NULL,
    expression_latex TEXT NOT NULL,
    expression_normalized TEXT,
    source_row_id INTEGER REFERENCES source_rows(id) ON DELETE SET NULL,
    confidence TEXT NOT NULL DEFAULT 'seeded',
    notes TEXT,
    UNIQUE (function_id, expression_kind, expression_latex)
);

CREATE VIEW IF NOT EXISTS v_function_external_ids AS
SELECT
    f.stable_id,
    f.dimension,
    f.field_label,
    f.formula_latex,
    e.id_kind,
    e.external_id,
    p.slug AS source_page,
    t.slug AS source_table,
    r.row_number AS source_row_number
FROM apn_functions f
JOIN source_row_function_links l ON l.function_id = f.id
JOIN source_rows r ON r.id = l.source_row_id
JOIN source_external_ids e ON e.source_row_id = r.id
JOIN source_tables t ON t.id = r.source_table_id
JOIN source_pages p ON p.id = t.page_id;

CREATE VIEW IF NOT EXISTS v_function_invariants AS
SELECT
    f.stable_id,
    f.formula_latex,
    f.dimension,
    it.slug AS invariant_slug,
    it.label AS invariant_label,
    fi.value_text,
    fi.numeric_value,
    p.slug AS source_page,
    t.slug AS source_table,
    r.row_number AS source_row_number,
    fi.notes
FROM function_invariants fi
JOIN apn_functions f ON f.id = fi.function_id
JOIN invariant_types it ON it.id = fi.invariant_type_id
JOIN source_rows r ON r.id = fi.source_row_id
JOIN source_tables t ON t.id = r.source_table_id
JOIN source_pages p ON p.id = t.page_id;

CREATE VIEW IF NOT EXISTS v_resolved_source_references AS
SELECT
    p.slug AS source_page,
    t.slug AS source_table,
    r.row_number AS source_row_number,
    r.raw_label AS source_row_label,
    r.raw_value AS source_row_value,
    rt.slug AS referenced_source_table,
    ref.id_kind,
    ref.external_id,
    f.stable_id,
    f.formula_latex,
    ref.resolution_note
FROM source_references ref
JOIN source_rows r ON r.id = ref.source_row_id
JOIN source_tables t ON t.id = r.source_table_id
JOIN source_pages p ON p.id = t.page_id
JOIN source_tables rt ON rt.id = ref.referenced_source_table_id
LEFT JOIN apn_functions f ON f.id = ref.function_id;

CREATE VIEW IF NOT EXISTS v_apn_function_summary AS
SELECT
    f.stable_id,
    f.dimension,
    f.field_label,
    f.formula_latex,
    GROUP_CONCAT(DISTINCT e.external_id) AS source_ids,
    GROUP_CONCAT(DISTINCT it.label || '=' || fi.value_text) AS invariants
FROM apn_functions f
LEFT JOIN source_row_function_links l ON l.function_id = f.id
LEFT JOIN source_rows r ON r.id = l.source_row_id
LEFT JOIN source_external_ids e ON e.source_row_id = r.id
LEFT JOIN function_invariants fi ON fi.function_id = f.id
LEFT JOIN invariant_types it ON it.id = fi.invariant_type_id
GROUP BY
    f.id,
    f.stable_id,
    f.dimension,
    f.field_label,
    f.formula_latex;

CREATE VIEW IF NOT EXISTS v_apn_function_ccz_invariants AS
SELECT
    f.id AS function_id,
    f.stable_id,
    f.dimension,
    f.field_label,
    f.formula_latex,
    g.gamma_rank,
    d.delta_rank,
    m.multiplier_group_order
FROM apn_functions f
LEFT JOIN function_gamma_ranks g ON g.function_id = f.id
LEFT JOIN function_delta_ranks d ON d.function_id = f.id
LEFT JOIN function_multiplier_group_orders m ON m.function_id = f.id;
