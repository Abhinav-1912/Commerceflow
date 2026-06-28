from __future__ import annotations

import pandas as pd

from utils.logger import get_logger
from utils.validators import (
    REQUIRED_CUSTOMER_COLUMNS,
    REQUIRED_TRANSACTION_COLUMNS,
    validate_columns,
    validate_non_empty,
)

logger = get_logger(__name__)


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df, REQUIRED_TRANSACTION_COLUMNS, "transactions")
    validate_non_empty(df, "transactions")

    out = df.copy()
    out["transaction_ts"] = pd.to_datetime(out["transaction_ts"], utc=True, errors="coerce")
    out["amount"] = pd.to_numeric(out["amount"], errors="coerce")
    out = out.dropna(subset=["transaction_id", "customer_id", "transaction_ts", "amount"])
    out["status"] = out["status"].str.upper().fillna("UNKNOWN")
    out = out[out["amount"] >= 0]
    out = out.drop_duplicates(subset=["transaction_id"])

    logger.info("Cleaned transactions: %s rows", len(out))
    return out


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df, REQUIRED_CUSTOMER_COLUMNS, "customers")
    validate_non_empty(df, "customers")

    out = df.copy()
    out["signup_date"] = pd.to_datetime(out["signup_date"], errors="coerce").dt.date
    out = out.dropna(subset=["customer_id", "email"])
    out = out.drop_duplicates(subset=["customer_id"])

    logger.info("Cleaned customers: %s rows", len(out))
    return out


def build_fact_transactions(transactions: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    cust_cols = ["customer_id", "country", "signup_date"]
    merged = transactions.merge(customers[cust_cols], on="customer_id", how="left")
    merged["transaction_date"] = merged["transaction_ts"].dt.date
    merged["is_high_value"] = (merged["amount"] >= 2000).astype(int)

    logger.info("Built fact transactions: %s rows", len(merged))
    return merged
