from __future__ import annotations

import csv
import json
from pathlib import Path
import sqlite3
from typing import Dict, Iterable, List


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_jsonl(rows: Iterable[Dict[str, str]], path: Path) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


def write_csv(rows: List[Dict[str, str]], path: Path) -> None:
    ensure_dir(path.parent)
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def upsert_sqlite(rows: List[Dict[str, str]], table_name: str, sqlite_path: Path) -> None:
    ensure_dir(sqlite_path.parent)
    if not rows:
        return
    columns = list(rows[0].keys())
    column_defs = ", ".join([f'"{c}" TEXT' for c in columns])
    placeholders = ", ".join(["?" for _ in columns])
    insert_sql = f'INSERT INTO "{table_name}" ({", ".join([f"\"{c}\"" for c in columns])}) VALUES ({placeholders})'

    conn = sqlite3.connect(sqlite_path)
    try:
        conn.execute(f'DROP TABLE IF EXISTS "{table_name}"')
        conn.execute(f'CREATE TABLE "{table_name}" ({column_defs})')
        conn.executemany(insert_sql, [[row.get(c, "") for c in columns] for row in rows])
        conn.commit()
    finally:
        conn.close()
