from __future__ import annotations


def transform_transactions(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    transformed: list[dict[str, object]] = []

    for row in rows:
        quantity = int(row["quantity"])
        unit_price = float(row["unit_price"])
        amount = round(quantity * unit_price, 2)
        is_high_value = amount >= 1000
        is_suspicious = is_high_value and str(row["payment_method"]).lower() == "cod"

        transformed.append(
            {
                **row,
                "transaction_amount": amount,
                "is_high_value": int(is_high_value),
                "is_suspicious": int(is_suspicious),
            }
        )

    return transformed
