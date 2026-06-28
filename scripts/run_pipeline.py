from __future__ import annotations

import argparse
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

from scripts.etl.extract import read_csv_from_s3, seed_sample_files, write_df_to_s3_csv
from scripts.etl.load import execute_redshift_sql
from scripts.etl.transform import build_fact_transactions, clean_customers, clean_transactions
from utils.logger import get_logger

logger = get_logger(__name__)


def load_config() -> dict:
    root = Path(__file__).resolve().parents[1]
    with open(root / "config" / "pipeline_config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_sql(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def run_seed(config: dict) -> None:
    bucket = os.environ["S3_BUCKET"]
    raw_prefix = os.environ["S3_RAW_PREFIX"]
    seed_sample_files(bucket, raw_prefix, config)


def run_etl(config: dict) -> None:
    bucket = os.environ["S3_BUCKET"]
    raw_prefix = os.environ["S3_RAW_PREFIX"]
    processed_prefix = os.environ["S3_PROCESSED_PREFIX"]
    curated_prefix = os.environ["S3_CURATED_PREFIX"]

    tx_key = f"{raw_prefix.rstrip('/')}/{config['s3']['raw_transactions_key']}"
    cust_key = f"{raw_prefix.rstrip('/')}/{config['s3']['raw_customers_key']}"

    transactions = read_csv_from_s3(bucket, tx_key)
    customers = read_csv_from_s3(bucket, cust_key)

    transactions_clean = clean_transactions(transactions)
    customers_clean = clean_customers(customers)
    fact_transactions = build_fact_transactions(transactions_clean, customers_clean)

    processed_tx_key = f"{processed_prefix.rstrip('/')}/{config['s3']['processed_transactions_key']}"
    curated_fact_key = f"{curated_prefix.rstrip('/')}/{config['s3']['curated_facts_key']}"
    curated_dim_key = f"{curated_prefix.rstrip('/')}/{config['s3']['curated_dim_customers_key']}"

    write_df_to_s3_csv(transactions_clean, bucket, processed_tx_key)
    write_df_to_s3_csv(fact_transactions, bucket, curated_fact_key)
    write_df_to_s3_csv(customers_clean, bucket, curated_dim_key)


def run_redshift_sql() -> None:
    root = Path(__file__).resolve().parents[1]
    redshift_dir = root / "scripts" / "redshift"

    for file_name in ["ddl.sql", "analytics.sql", "fraud_detection.sql"]:
        sql = read_sql(redshift_dir / file_name)
        execute_redshift_sql(sql)
        logger.info("Executed %s", file_name)


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Run CommerceFlow pipeline")
    parser.add_argument("--stage", choices=["seed", "etl", "sql", "all"], default="all")
    args = parser.parse_args()

    config = load_config()

    if args.stage in {"seed", "all"}:
        run_seed(config)
    if args.stage in {"etl", "all"}:
        run_etl(config)
    if args.stage in {"sql", "all"}:
        run_redshift_sql()

    logger.info("Pipeline execution completed for stage=%s", args.stage)


if __name__ == "__main__":
    main()
