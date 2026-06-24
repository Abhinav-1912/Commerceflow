from __future__ import annotations


REQUIRED_FIELDS = {
    "transaction_id",
    "customer_id",
    "timestamp",
    "product_id",
    "quantity",
    "unit_price",
    "payment_method",
    "country",
    "transaction_amount",
    "is_high_value",
    "is_suspicious",
}


def validate_transactions(rows: list[dict[str, object]]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    seen_ids: set[str] = set()

    for idx, row in enumerate(rows):
        row_no = idx + 1
        missing = REQUIRED_FIELDS.difference(row.keys())
        if missing:
            errors.append(f"row {row_no}: missing fields {sorted(missing)}")
            continue

        transaction_id = str(row["transaction_id"])
        if transaction_id in seen_ids:
            errors.append(f"row {row_no}: duplicate transaction_id {transaction_id}")
        seen_ids.add(transaction_id)

        if int(row["quantity"]) <= 0:
            errors.append(f"row {row_no}: quantity must be positive")

        if float(row["unit_price"]) <= 0:
            errors.append(f"row {row_no}: unit_price must be positive")

        if round(float(row["transaction_amount"]), 2) != round(
            int(row["quantity"]) * float(row["unit_price"]),
            2,
        ):
            errors.append(f"row {row_no}: transaction_amount mismatch")

    return (len(errors) == 0, errors)
