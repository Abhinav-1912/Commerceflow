import unittest

from commerceflow.etl import clean_transactions


class TestETL(unittest.TestCase):
    def test_clean_transactions_adds_fields(self):
        rows = [
            {
                "transaction_id": "TXN-1",
                "customer_id": "C1",
                "event_ts": "2026-01-01T10:00:00+00:00",
                "amount": "120.127",
                "billing_country": "US",
                "ip_country": "US",
                "status": "approved",
            }
        ]
        cleaned = clean_transactions(rows, high_value_threshold=100)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned[0]["amount"], "120.13")
        self.assertEqual(cleaned[0]["event_date"], "2026-01-01")
        self.assertEqual(cleaned[0]["is_high_value"], "true")


if __name__ == "__main__":
    unittest.main()
