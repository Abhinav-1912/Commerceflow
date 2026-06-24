from __future__ import annotations

from pathlib import Path
from typing import Dict

from .config import Settings
from .data_simulation import generate_transactions
from .etl import clean_transactions
from .fraud import detect_fraud
from .io import upsert_sqlite, write_csv, write_jsonl


def run_pipeline(transaction_count: int = 1000, seed: int = 42) -> Dict[str, str]:
    settings = Settings()
    raw = generate_transactions(count=transaction_count, seed=seed)

    if settings.fail_on_empty and not raw:
        raise ValueError("No transactions generated")

    curated = clean_transactions(raw, high_value_threshold=settings.high_value_threshold)
    scored = detect_fraud(curated, high_value_threshold=settings.high_value_threshold)

    base = Path(settings.output_dir)
    raw_path = base / "raw" / "transactions.jsonl"
    curated_path = base / "curated" / "transactions_scored.csv"
    sqlite_path = base / "warehouse" / "commerceflow.db"

    write_jsonl(raw, raw_path)
    write_csv(scored, curated_path)
    upsert_sqlite(scored, "fact_transactions", sqlite_path)

    return {
        "raw_path": str(raw_path),
        "curated_path": str(curated_path),
        "warehouse_path": str(sqlite_path),
        "row_count": str(len(scored)),
    }
