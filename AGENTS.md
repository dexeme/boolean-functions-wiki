# AGENTS.md

Guidance for AI agents working in this repository.

## Environment Notes

The Codex shell environment may be minimal.

Do not start responses with generic environment warnings such as:
"the shell environment is very minimal".

If common tools are missing, silently fall back to simple shell commands, absolute paths, or direct file inspection.

Only mention environment limitations when they block inspection, editing, or verification.

## Project Overview

This repository builds a Sphinx-based Boolean Functions wiki, with emphasis on APN functions and tables extracted from the Boolean Functions wiki. The checked-in content confirms a pipeline centered on raw wiki text in `data/`, derived reStructuredText pages in `docs/content/pages/`, CSV tables in `docs/content/tables/`, code examples in `docs/content/codes/` and `docs/sage-math/`, and a static Sphinx HTML build.

Project notes in `instructions.md` describe the goal of mapping Boolean Functions wiki tables into structured data while preserving provenance and enabling relationships between APN functions, invariants, equivalence classes, references, and source tables. Preserve that modeling direction when adding database or import work.

## Domain Rules

- Preserve source provenance.
- Do not assume that IDs from different wiki tables are globally equivalent unless explicitly documented.
- Keep raw imported data before normalization.
- Separate source tables/rows from parsed mathematical entities.
- Mathematical expressions may appear as LaTeX.
- Preserve original formulas when importing.
- Prefer explicit links between entities instead of implicit string matching.
- Be careful with APN, CCZ-equivalence, EA-equivalence, invariants, dimensions, finite fields, and references.

## Repository Layout

- `data/`: raw or partially raw extracted Boolean Functions wiki page text. Treat this as source material, not normalized data.
- `docs/`: Sphinx site tree. It contains the Sphinx configuration and build entry points, content pages, CSV-backed tables, custom extensions, static assets, generated APN table chunks, and Sage/code RST pages.
- `docs/conf.py`: Sphinx configuration. It enables MathJax, custom extensions from `docs/_ext`, and the classic HTML theme.
- `docs/Makefile`, `docs/make.bat`: Sphinx build entry points.
- `docs/index.rst`: main table of contents for code pages, Sage pages, and content pages.
- `docs/content/pages/`: generated or curated `.rst` pages for wiki content. Many pages link back to the original Boolean Functions wiki pages and reference extracted source files in `data/`.
- `docs/content/tables/`: CSV tables used by Sphinx pages. Examples include APN instance tables, CCZ invariant tables, and known APN family tables.
- `docs/content/codes/`: reStructuredText pages containing code-oriented content.
- `docs/sage-math/`: large SageMath-oriented `.rst` pages and code maps.
- `docs/_ext/`: custom Sphinx extensions, including `lazy_chunks.py`, which extends CSV rendering/chunking behavior.
- `docs/_static/`: CSS, JavaScript, and generated static chunks for large APN tables.
- `map/`: `.rst` mapping files for code/table-oriented content.
- `codes/test.py`: Sage/Python script for finite-field and APN-related computations. It is not currently a conventional pytest test file.
- `src/`: contains empty `codes/` and `content/` directories at the time this file was created.
- `content/`: empty at the time this file was created.
- `.github/workflows/sphinx.yml`: GitHub Actions workflow that builds Sphinx HTML and deploys `docs/build/html` from `main`.
- `requirements.txt`: Python docs/test dependencies. SageMath is noted as a separate environment requirement.
- `build/`, `docs/build/`, `.venv/`, `venv/`, `.pytest_cache/`, `.idea/`: generated or local environment directories. Avoid editing these for source changes.

Unknown / not currently present:

- No committed database schema, migration directory, or `.sql`/SQLite database files were found.
- No conventional `tests/` directory was found.
- No dedicated import script directory was found. Existing import/extraction logic may be embedded in generated artifacts or outside this repository.

## Data and Import Workflow

- Treat `data/` files as raw source captures. Do not overwrite or normalize them in place.
- Store extracted CSV tables under `docs/content/tables/` only when they preserve the source table structure closely enough to audit against the original page.
- For each imported table, keep references to the original wiki page URL and the local source file from `data/` in the corresponding `.rst` page or future source metadata tables.
- Preserve original row values and formulas exactly, including LaTeX/backtick math, before adding parsed fields.
- If a parsed value is uncertain, record it as uncertain with evidence instead of silently coercing it.
- Add validation scripts when changing import behavior. At minimum, validate CSV parseability, expected headers, row counts where known, duplicate local IDs within a source table, and references to source pages/tables.
- Detect duplicates explicitly. Distinguish duplicate source rows, duplicate formulas, and mathematically equivalent APN functions; these are not automatically the same fact.
- Prefer explicit relationship records such as source page -> source table -> source row -> parsed entity. Do not infer cross-table relationships from matching strings alone.

## Database Rules

There is no committed database schema or migration system at the time this file was created. If one is added:

- Inspect the current schema before changing it.
- Use new migrations instead of editing old migrations.
- Avoid destructive migrations.
- Preserve raw source rows.
- Use stable internal IDs for parsed entities such as APN functions, invariants, equivalence classes, references, and source tables.
- Do not rely only on wiki row numbers as global identifiers. Wiki IDs are local/external identifiers unless a source explicitly says otherwise.
- Add indexes only when needed for real lookup/query patterns.
- Keep source tables/rows separate from normalized mathematical entities.
- Make provenance columns or relation tables first-class, not comments.

## Sphinx and Docs Rules

- Build docs from `docs/`.
- Generated large-table HTML chunks live under `docs/_static/apn_chunks/`.
- CSV-backed pages should use Sphinx table directives and the local custom extensions rather than hardcoding large tables directly into `.rst` pages.
- When schema, import, or CSV files change, update the relevant `docs/content/pages/*.rst` page so it points to the correct source file, original wiki page, generated CSV, and references.
- Keep MathJax-friendly formulas intact. Many table cells use backtick-delimited math such as `` `x^{3}` ``.
- Avoid editing `docs/build/` or root `build/` as source; those are generated outputs.

Useful docs commands:

- `cd docs && make html`
- `cd docs && make livehtml`
- `sphinx-build -M html docs docs/build`

## Coding Rules

- Make small, focused changes.
- Follow existing style.
- Do not perform unrelated refactors.
- Do not add new dependencies unless necessary.
- Keep code and identifiers in English unless the existing file already uses another convention.
- Prefer standard Python CSV/parsing APIs over ad hoc string splitting.
- Keep generated files separate from source scripts when introducing import tooling.
- SageMath-dependent code should clearly state that SageMath must be installed separately.

## Generated Files

Do not edit generated build outputs directly.

Avoid editing:

- `docs/build/`
- `build/`
- `.pytest_cache/`
- `.venv/`
- `venv/`
- `.idea/`

If a generated file must change, update the source file or generation script instead.

## Large Table Rules

For large wiki tables:

- Do not manually rewrite large tables directly in `.rst` files.
- Prefer CSV-backed tables or generated chunks.
- Preserve original row order unless there is a documented reason to sort.
- Preserve original formulas exactly.
- Validate row counts after conversion when the source provides an expected count.
- Keep a reference to the source page and source table for every converted table.

## Entity Modeling Rules

When adding structured data, model at least two layers:

1. Source layer:
   - wiki page
   - source table
   - source row
   - source column
   - raw cell value

2. Parsed mathematical layer:
   - APN function
   - finite field dimension
   - polynomial/formula
   - invariant
   - equivalence class
   - reference

Do not collapse these two layers into a single table unless the task explicitly asks for a quick prototype.

## Math Formatting Rules

Many formulas are stored as backtick-delimited LaTeX, for example:

`x^{3}`

## Verification

Run only the commands relevant to the files changed.

Primary docs verification:

```bash
cd docs && make html
```

Alternative docs verification, if make is unavailable:

```bash
 html docs docs/build
```

CSV parse validation:
    
```
python - <<'PY'
import csv
from pathlib import Path

for path in Path("docs/content/tables").glob("*.csv"):
    with path.open(newline="", encoding="utf-8") as handle:
        list(csv.reader(handle))
    print(path)
PY
```

Unknown / not configured:

- No conventional test command is currently defined.
- Do not run pytest as the default verification unless a test suite is added.
- No formatter/linter command is currently defined.
- No database validation command is currently defined.

## Final Response Format

Future Codex responses for repository changes should end with:

Summary:
- ...

Changed files:
- ...

Verification:
- Command run: ...
- Result: ...

Not run:
- ...

Notes / risks:
- ...

If verification could not be run, explain why.