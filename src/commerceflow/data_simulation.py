from __future__ import annotations

from datetime import datetime, timedelta, timezone
import random
from typing import Dict, List


def generate_customers(count: int = 100, seed: int = 42) -> List[Dict[str, str]]:
    random.seed(seed)
    countries = ["US", "IN", "DE", "GB", "CA", "AU"]
    return [
        {
            "customer_id": f"CUST-{i:05d}",
            "segment": random.choice(["new", "returning", "vip"]),
            "country": random.choice(countries),
        }
        for i in range(1, count + 1)
    ]


def generate_transactions(
    count: int = 1000,
    seed: int = 42,
    start_time: datetime | None = None,
) -> List[Dict[str, str]]:
    random.seed(seed)
    customers = generate_customers(count=120, seed=seed)
    payment_methods = ["card", "wallet", "upi", "bank_transfer"]
    statuses = ["approved", "approved", "approved", "declined"]
    currencies = ["USD", "EUR", "INR"]

    baseline = start_time or datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    rows: List[Dict[str, str]] = []

    for i in range(1, count + 1):
        customer = random.choice(customers)
        event_ts = baseline + timedelta(seconds=i * random.randint(5, 25))
        amount = round(max(5.0, random.lognormvariate(3.2, 0.8)), 2)
        rows.append(
            {
                "transaction_id": f"TXN-{i:08d}",
                "customer_id": customer["customer_id"],
                "event_ts": event_ts.isoformat(),
                "amount": str(amount),
                "currency": random.choice(currencies),
                "payment_method": random.choice(payment_methods),
                "billing_country": customer["country"],
                "ip_country": random.choice([customer["country"], customer["country"], "NG", "BR"]),
                "device_id": f"DEV-{random.randint(1, 300):04d}",
                "status": random.choice(statuses),
            }
        )
    return rows
