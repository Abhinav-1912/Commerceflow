from __future__ import annotations

import pandas as pd


REQUIRED_TRANSACTION_COLUMNS = {
    "transaction_id",
    "customer_id",
    "transaction_ts",
    "amount",
    "currency",
    "payment_method",
    "ip_address",
    "device_id",
    "status",
}

REQUIRED_CUSTOMER_COLUMNS = {
    "customer_id",
    "first_name",
    "last_name",
    "email",
    "country",
    "signup_date",
}


def validate_columns(df: pd.DataFrame, required: set[str], name: str) -> None:
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{name} missing columns: {sorted(missing)}")


def validate_non_empty(df: pd.DataFrame, name: str) -> None:
    if df.empty:
        raise ValueError(f"{name} is empty")
