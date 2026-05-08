#!/bin/bash
set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]}"
case "$SCRIPT_PATH" in
    /*) SCRIPT_DIR="${SCRIPT_PATH%/*}" ;;
    */*) SCRIPT_DIR="$PWD/${SCRIPT_PATH%/*}" ;;
    *) SCRIPT_DIR="$PWD" ;;
esac
ROOT_DIR="$(CDPATH= cd -- "$SCRIPT_DIR" && pwd)"
DB_PATH="${1:-"$ROOT_DIR/db/build/boolean-functions.sqlite3"}"

find_tool() {
    local name="$1"
    shift

    if command -v "$name" >/dev/null 2>&1; then
        command -v "$name"
        return 0
    fi

    local candidate
    for candidate in "$@"; do
        if [ -x "$candidate" ]; then
            printf '%s\n' "$candidate"
            return 0
        fi
    done

    printf 'Missing required command: %s\n' "$name" >&2
    return 1
}

PYTHON_BIN="$(find_tool python3 /bin/python3 /usr/bin/python3)"
SQLITE_BIN="$(find_tool sqlite3 /bin/sqlite3 /usr/bin/sqlite3)"
MKTEMP_BIN="$(find_tool mktemp /bin/mktemp /usr/bin/mktemp)"
MKDIR_BIN="$(find_tool mkdir /bin/mkdir /usr/bin/mkdir)"
MV_BIN="$(find_tool mv /bin/mv /usr/bin/mv)"
RM_BIN="$(find_tool rm /bin/rm /usr/bin/rm)"

TMP_DB="$("$MKTEMP_BIN" "${TMPDIR:-/tmp}/boolean-functions.XXXXXX.sqlite3")"
cleanup() {
    "$RM_BIN" -f "$TMP_DB"
}
trap cleanup EXIT

cd "$ROOT_DIR"

printf 'Regenerating derived SQL...\n'
"$PYTHON_BIN" db/scripts/generate_import_ccz_invariants_n7.py

printf 'Building temporary database: %s\n' "$TMP_DB"
"$SQLITE_BIN" "$TMP_DB" <<'SQL'
.read db/sql/schema.sql
.read db/sql/seed.sql
.read db/sql/import_apn_n7.sql
.read db/generated/import_ccz_invariants_n7.sql
SQL

printf 'Running checks...\n'
"$SQLITE_BIN" "$TMP_DB" <<'SQL'
.headers on
.mode column

SELECT 'apn_functions' AS check_name, COUNT(*) AS actual, 490 AS expected
FROM apn_functions;

SELECT 'function_gamma_ranks' AS check_name, COUNT(*) AS actual, 490 AS expected
FROM function_gamma_ranks;

SELECT 'function_delta_ranks' AS check_name, COUNT(*) AS actual, 490 AS expected
FROM function_delta_ranks;

SELECT 'function_multiplier_group_orders' AS check_name, COUNT(*) AS actual, 490 AS expected
FROM function_multiplier_group_orders;

SELECT 'wide_view_complete_rows' AS check_name, COUNT(*) AS actual, 490 AS expected
FROM v_apn_function_ccz_invariants
WHERE gamma_rank IS NOT NULL
  AND delta_rank IS NOT NULL
  AND multiplier_group_order IS NOT NULL;

SELECT
    stable_id,
    gamma_rank,
    delta_rank,
    multiplier_group_order
FROM v_apn_function_ccz_invariants
WHERE stable_id IN ('apn-gf-2-7-0001', 'apn-gf-2-7-0002')
ORDER BY stable_id;
SQL

check_count() {
    local sql="$1"
    local expected="$2"
    local actual
    actual="$("$SQLITE_BIN" "$TMP_DB" "$sql")"
    if [ "$actual" != "$expected" ]; then
        printf 'Check failed. Expected %s, got %s.\nSQL: %s\n' "$expected" "$actual" "$sql" >&2
        exit 1
    fi
}

check_count "SELECT COUNT(*) FROM apn_functions;" "490"
check_count "SELECT COUNT(*) FROM function_gamma_ranks;" "490"
check_count "SELECT COUNT(*) FROM function_delta_ranks;" "490"
check_count "SELECT COUNT(*) FROM function_multiplier_group_orders;" "490"
check_count "SELECT COUNT(*) FROM v_apn_function_ccz_invariants WHERE gamma_rank IS NOT NULL AND delta_rank IS NOT NULL AND multiplier_group_order IS NOT NULL;" "490"
check_count "SELECT COUNT(*) FROM v_apn_function_ccz_invariants WHERE gamma_rank = 3610;" "2"

DB_DIR="${DB_PATH%/*}"
if [ "$DB_DIR" = "$DB_PATH" ]; then
    DB_DIR="."
fi
"$MKDIR_BIN" -p "$DB_DIR"
"$MV_BIN" "$TMP_DB" "$DB_PATH"
trap - EXIT

printf 'Database rebuilt successfully: %s\n' "$DB_PATH"
printf 'DataGrip: connect to exactly this SQLite file.\n'
