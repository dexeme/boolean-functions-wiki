PRAGMA foreign_keys = ON;

CREATE TEMP TABLE imported_apn_function_properties_raw (
    raw_line TEXT
);

.mode list
.separator "\t"
.import --skip 1 db/data/apn_function_properties.csv imported_apn_function_properties_raw

CREATE TEMP VIEW imported_apn_function_properties AS
WITH parsed AS (
    SELECT
        raw_line,
        INSTR(raw_line, ',') AS first_comma
    FROM imported_apn_function_properties_raw
),
first_split AS (
    SELECT
        raw_line,
        CASE
            WHEN first_comma > 0 THEN SUBSTR(raw_line, 1, first_comma - 1)
            ELSE raw_line
        END AS first_column,
        CASE
            WHEN first_comma > 0 THEN SUBSTR(raw_line, first_comma + 1)
            ELSE ''
        END AS rest_after_first
    FROM parsed
),
second_split AS (
    SELECT
        raw_line,
        first_column,
        CASE
            WHEN INSTR(rest_after_first, ',') > 0 THEN SUBSTR(rest_after_first, 1, INSTR(rest_after_first, ',') - 1)
            ELSE rest_after_first
        END AS second_column,
        CASE
            WHEN INSTR(rest_after_first, ',') > 0 THEN SUBSTR(rest_after_first, INSTR(rest_after_first, ',') + 1)
            ELSE ''
        END AS rest_after_second
    FROM first_split
),
third_split AS (
    SELECT
        raw_line,
        first_column,
        second_column,
        CASE
            WHEN INSTR(rest_after_second, ',') > 0 THEN SUBSTR(rest_after_second, 1, INSTR(rest_after_second, ',') - 1)
            ELSE rest_after_second
        END AS third_column,
        CASE
            WHEN INSTR(rest_after_second, ',') > 0 THEN SUBSTR(rest_after_second, INSTR(rest_after_second, ',') + 1)
            ELSE NULL
        END AS fourth_column
    FROM second_split
)
SELECT
    CASE
        WHEN TRIM(first_column) LIKE 'apn-gf-%' THEN NULLIF(TRIM(first_column), '')
        ELSE NULL
    END AS stable_id,
    CASE
        WHEN TRIM(first_column) LIKE 'apn-gf-%' THEN NULL
        ELSE CAST(NULLIF(TRIM(first_column), '') AS INTEGER)
    END AS dimension,
    CASE
        WHEN TRIM(first_column) LIKE 'apn-gf-%' THEN NULL
        ELSE NULLIF(TRIM(second_column), '')
    END AS function_label,
    CASE
        WHEN TRIM(first_column) LIKE 'apn-gf-%' THEN NULLIF(TRIM(second_column), '')
        ELSE NULLIF(TRIM(third_column), '')
    END AS equivalent_to,
    CASE
        WHEN TRIM(first_column) LIKE 'apn-gf-%' THEN NULLIF(TRIM(third_column), '')
        ELSE NULLIF(TRIM(fourth_column), '')
    END AS walsh_spectrum
FROM third_split
WHERE NULLIF(TRIM(first_column), '') IS NOT NULL;

UPDATE apn_functions
SET
    equivalent_to = COALESCE(
        (
            SELECT NULLIF(TRIM(p.equivalent_to), '')
            FROM imported_apn_function_properties p
            WHERE
                NULLIF(TRIM(p.equivalent_to), '') IS NOT NULL
                AND (
                    NULLIF(TRIM(p.stable_id), '') = apn_functions.stable_id
                    OR EXISTS (
                        SELECT 1
                        FROM source_row_function_links l
                        JOIN source_external_ids e ON e.source_row_id = l.source_row_id
                        WHERE l.function_id = apn_functions.id
                          AND apn_functions.dimension = p.dimension
                          AND e.id_kind IN ('wiki_id', 'function_label')
                          AND e.external_id = p.function_label
                    )
                )
            LIMIT 1
        ),
        equivalent_to
    ),
    walsh_spectrum = COALESCE(
        (
            SELECT NULLIF(TRIM(p.walsh_spectrum), '')
            FROM imported_apn_function_properties p
            WHERE
                NULLIF(TRIM(p.walsh_spectrum), '') IS NOT NULL
                AND (
                    NULLIF(TRIM(p.stable_id), '') = apn_functions.stable_id
                    OR EXISTS (
                        SELECT 1
                        FROM source_row_function_links l
                        JOIN source_external_ids e ON e.source_row_id = l.source_row_id
                        WHERE l.function_id = apn_functions.id
                          AND apn_functions.dimension = p.dimension
                          AND e.id_kind IN ('wiki_id', 'function_label')
                          AND e.external_id = p.function_label
                    )
                )
            LIMIT 1
        ),
        walsh_spectrum
    )
WHERE EXISTS (
    SELECT 1
    FROM imported_apn_function_properties p
    WHERE
        NULLIF(TRIM(p.stable_id), '') = apn_functions.stable_id
        OR EXISTS (
            SELECT 1
            FROM source_row_function_links l
            JOIN source_external_ids e ON e.source_row_id = l.source_row_id
            WHERE l.function_id = apn_functions.id
              AND apn_functions.dimension = p.dimension
              AND e.id_kind IN ('wiki_id', 'function_label')
              AND e.external_id = p.function_label
        )
);
