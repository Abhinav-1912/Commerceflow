from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, Iterable, List


def clean_transactions(rows: Iterable[Dict[str, str]], high_value_threshold: float) -> List[Dict[str, str]]:
    cleaned: List[Dict[str, str]] = []

    for row in rows:
        if row.get("status") not in {"approved", "declined"}:
            continue
        try:
            amount = round(float(row["amount"]), 2)
            event_ts = datetime.fromisoformat(row["event_ts"])
        except (KeyError, ValueError):
            continue

        cleaned.append(
            {
                **row,
                "amount": f"{amount:.2f}",
                "event_ts": event_ts.astimezone(timezone.utc).isoformat(),
                "event_date": event_ts.date().isoformat(),
                "ingestion_ts": datetime.now(timezone.utc).isoformat(),
                "is_high_value": str(amount >= high_value_threshold).lower(),
            }
        )
    return cleaned
