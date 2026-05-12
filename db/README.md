# SQLite Database

This directory contains the SQLite schema and import scripts for the APN function database.

## Layout

- `sql/schema.sql`: schema, indexes, and views.
- `sql/seed.sql`: source page/table seed data for the APN dimension 7 function list.
- `sql/import_apn_n7.sql`: imports the 490 APN functions from `docs/content/tables/known_instances_apn_gf2_7.csv`.
- `sql/import_apn_function_properties.sql`: imports manually maintained APN function properties from `db/data/apn_function_properties.csv`.
- `data/apn_function_properties.csv`: optional properties for existing APN functions, keyed by `stable_id` or wiki ID.
- `scripts/generate_import_ccz_invariants_n7.py`: regenerates the CCZ invariant import SQL from the three CSV files.
- `generated/import_ccz_invariants_n7.sql`: generated SQL for Gamma-rank, Delta-rank, and Multiplier group order.
- `build/boolean-functions.sqlite3`: generated SQLite database. Connect DataGrip to this file.

## Rebuild

From the repository root, run:

```bash
./script.sh
```

The script will:

- regenerate `db/generated/import_ccz_invariants_n7.sql`;
- rebuild `db/build/boolean-functions.sqlite3` from scratch;
- apply optional APN function properties from `db/data/apn_function_properties.csv`;
- verify that all 490 APN functions have Gamma-rank, Delta-rank, and Multiplier group order;
- print the exact SQLite path to use in DataGrip.

## DataGrip

Connect DataGrip to exactly this file:

```text
/home/tiago/tcc/boolean-functions-wiki/db/build/boolean-functions.sqlite3
```

After connecting or rebuilding, use **Synchronize** / refresh on the DataGrip data source.

The main view for filtering is:

```sql
v_apn_function_ccz_invariants
```

Example:

```sql
SELECT
    stable_id,
    formula_latex,
    equivalent_to,
    walsh_spectrum,
    gamma_rank,
    delta_rank,
    multiplier_group_order
FROM v_apn_function_ccz_invariants
WHERE stable_id = 'apn-gf-2-7-0474';
```

If you want to search by the wiki ID `474`:

```sql
SELECT
    v.stable_id,
    v.formula_latex,
    v.equivalent_to,
    v.walsh_spectrum,
    v.gamma_rank,
    v.delta_rank,
    v.multiplier_group_order
FROM v_apn_function_ccz_invariants v
JOIN v_function_external_ids e
    ON e.stable_id = v.stable_id
WHERE e.id_kind = 'wiki_id'
  AND e.external_id = '474';
```

## APN Function Properties

To register `equivalent_to` and `walsh_spectrum` for existing functions, edit `db/data/apn_function_properties.csv`.
Use either `stable_id` or `wiki_id` to identify the function:

```csv
stable_id,wiki_id,equivalent_to,walsh_spectrum
apn-gf-2-7-0474,,Gold function,Gold-like
,474,Gold function,Gold-like
```

Then rebuild the database:

```bash
./script.sh
```
