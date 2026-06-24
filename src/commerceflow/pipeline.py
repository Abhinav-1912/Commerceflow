from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from .cleaning import clean_transactions
from .config import load_aws_integration_config, load_pipeline_config
from .generator import generate_sample_transactions
from .ingestion import read_csv, write_csv
from .transformation import transform_transactions
from .validation import validate_transactions


def run_pipeline(config_path: str | Path, create_sample_if_missing: bool = True) -> dict[str, object]:
    cfg = load_pipeline_config(config_path)

    raw_path = Path(cfg.raw_input_path)
    if create_sample_if_missing and not raw_path.exists():
        generate_sample_transactions(raw_path)

    raw_rows = read_csv(raw_path)
    cleaned = clean_transactions(raw_rows)
    transformed = transform_transactions(cleaned)

    valid, errors = validate_transactions(transformed)
    if not valid:
        raise ValueError(f"Validation failed: {'; '.join(errors[:5])}")

    write_csv(cfg.bronze_output_path, raw_rows, list(raw_rows[0].keys()) if raw_rows else [])
    write_csv(cfg.silver_output_path, cleaned, list(cleaned[0].keys()) if cleaned else [])
    write_csv(cfg.gold_output_path, transformed, list(transformed[0].keys()) if transformed else [])

    return {
        "input_rows": len(raw_rows),
        "cleaned_rows": len(cleaned),
        "gold_rows": len(transformed),
        "output_files": {
            "bronze": cfg.bronze_output_path,
            "silver": cfg.silver_output_path,
            "gold": cfg.gold_output_path,
        },
    }


def load_aws_mapping(config_path: str | Path) -> dict[str, str]:
    aws_cfg = load_aws_integration_config(config_path)
    return asdict(aws_cfg)
