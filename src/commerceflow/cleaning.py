from __future__ import annotations

from datetime import datetime


def clean_transactions(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    cleaned: list[dict[str, object]] = []

    for row in rows:
        if not row.get("transaction_id") or not row.get("customer_id"):
            continue

        try:
            quantity = int(row["quantity"])
            unit_price = float(row["unit_price"])
            timestamp = datetime.fromisoformat(row["timestamp"]).isoformat()
        except (ValueError, KeyError, TypeError):
            continue

        if quantity <= 0 or unit_price <= 0:
            continue

        cleaned.append(
            {
                "transaction_id": row["transaction_id"].strip(),
                "customer_id": row["customer_id"].strip(),
                "timestamp": timestamp,
                "product_id": row["product_id"].strip(),
                "quantity": quantity,
                "unit_price": round(unit_price, 2),
                "payment_method": row["payment_method"].strip().lower(),
                "country": row["country"].strip().upper(),
            }
        )

    return cleaned
