from __future__ import annotations

from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Deque, Dict, List


def detect_fraud(rows: List[Dict[str, str]], high_value_threshold: float) -> List[Dict[str, str]]:
    tx_by_customer: Dict[str, Deque[datetime]] = defaultdict(deque)
    result: List[Dict[str, str]] = []

    ordered = sorted(rows, key=lambda r: r["event_ts"])
    for row in ordered:
        reasons: List[str] = []
        score = 0
        amount = float(row["amount"])
        event_ts = datetime.fromisoformat(row["event_ts"])

        if amount >= (high_value_threshold * 1.4):
            score += 40
            reasons.append("high_amount")

        if row.get("billing_country") and row.get("ip_country") and row["billing_country"] != row["ip_country"]:
            score += 25
            reasons.append("country_mismatch")

        customer_id = row.get("customer_id", "")
        history = tx_by_customer[customer_id]
        window_start = event_ts - timedelta(minutes=10)
        while history and history[0] < window_start:
            history.popleft()
        if len(history) >= 3:
            score += 30
            reasons.append("velocity_spike")
        history.append(event_ts)

        if row.get("status") == "declined":
            score += 20
            reasons.append("payment_declined")

        is_fraud = score >= 50
        result.append(
            {
                **row,
                "fraud_score": str(score),
                "fraud_reasons": ",".join(reasons),
                "is_fraud": str(is_fraud).lower(),
            }
        )

    return result
