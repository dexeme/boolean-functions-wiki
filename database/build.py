import argparse
import csv
import shutil
import subprocess
import sys
from pathlib import Path

from sqlite_utils import Database


ROOT_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT_DIR / "docs"
TABLES_DIR = DOCS_DIR / "content" / "tables"
HTML_DIR = DOCS_DIR / "_build" / "html"
DATABASE_DIR = HTML_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "boolean_wiki.db"
OLD_DATABASE_PATH = HTML_DIR / "boolean_wiki.db"


def build_docs():
    subprocess.run(
        [sys.executable, "-m", "sphinx", "-b", "html", str(DOCS_DIR), str(HTML_DIR)],
        check=True,
    )


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def write_database():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    for path in (DATABASE_PATH, OLD_DATABASE_PATH):
        if path.exists():
            path.unlink()

    database = Database(DATABASE_PATH)

    for csv_path in sorted(TABLES_DIR.glob("*.csv")):
        fields, rows = read_csv(csv_path)
        table = database[csv_path.stem]
        if rows:
            table.insert_all(rows, alter=True)
        elif fields:
            table.create({field: str for field in fields}, if_not_exists=True)


def clean_build():
    shutil.rmtree(HTML_DIR.parent, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()

    if args.clean:
        clean_build()

    build_docs()
    write_database()


if __name__ == "__main__":
    main()
