from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


HEADER = [
    "transaction_id",
    "customer_id",
    "timestamp",
    "product_id",
    "quantity",
    "unit_price",
    "payment_method",
    "country",
]

PAYMENT_METHODS = ["card", "wallet", "bank_transfer", "cod"]
COUNTRIES = ["US", "IN", "GB", "DE", "CA"]


def generate_sample_transactions(output_path: str | Path, num_rows: int = 200, seed: int = 7) -> None:
    random.seed(seed)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    start = datetime(2026, 1, 1, 0, 0, 0)
    with open(output_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADER)

        for i in range(1, num_rows + 1):
            quantity = random.randint(1, 5)
            # Include a few intentionally noisy rows for cleaning/validation coverage.
            if i % 55 == 0:
                quantity = -1

            row = [
                f"txn_{i:06d}",
                f"cust_{random.randint(1, 30):04d}",
                (start + timedelta(minutes=i * random.randint(1, 3))).isoformat(),
                f"prod_{random.randint(1, 50):04d}",
                quantity,
                round(random.uniform(5.0, 1200.0), 2),
                random.choice(PAYMENT_METHODS),
                random.choice(COUNTRIES),
            ]
            writer.writerow(row)
