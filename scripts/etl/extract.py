from __future__ import annotations

import io
import os
from pathlib import Path

import pandas as pd

from utils.aws_clients import get_s3_client
from utils.logger import get_logger

logger = get_logger(__name__)


def upload_local_file_to_s3(local_path: str, bucket: str, key: str) -> None:
    s3 = get_s3_client()
    logger.info("Uploading %s to s3://%s/%s", local_path, bucket, key)
    s3.upload_file(local_path, bucket, key)


def read_csv_from_s3(bucket: str, key: str) -> pd.DataFrame:
    s3 = get_s3_client()
    logger.info("Reading CSV from s3://%s/%s", bucket, key)
    obj = s3.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(io.BytesIO(obj["Body"].read()))


def write_df_to_s3_csv(df: pd.DataFrame, bucket: str, key: str) -> None:
    s3 = get_s3_client()
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    logger.info("Writing DataFrame to s3://%s/%s", bucket, key)
    s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue().encode("utf-8"))


def seed_sample_files(bucket: str, raw_prefix: str, config: dict) -> None:
    root = Path(__file__).resolve().parents[2]
    tx_local = root / "data" / "sample_transactions.csv"
    cust_local = root / "data" / "sample_customers.csv"

    tx_key = f"{raw_prefix.rstrip('/')}/{config['s3']['raw_transactions_key']}"
    cust_key = f"{raw_prefix.rstrip('/')}/{config['s3']['raw_customers_key']}"

    upload_local_file_to_s3(str(tx_local), bucket, tx_key)
    upload_local_file_to_s3(str(cust_local), bucket, cust_key)
