import unittest

from commerceflow.fraud import detect_fraud


class TestFraud(unittest.TestCase):
    def test_high_amount_and_country_mismatch_flags_fraud(self):
        rows = [
            {
                "transaction_id": "TXN-1",
                "customer_id": "C1",
                "event_ts": "2026-01-01T10:00:00+00:00",
                "amount": "800.00",
                "billing_country": "US",
                "ip_country": "NG",
                "status": "approved",
            }
        ]

        scored = detect_fraud(rows, high_value_threshold=500)
        self.assertEqual(scored[0]["is_fraud"], "true")
        self.assertIn("high_amount", scored[0]["fraud_reasons"])
        self.assertIn("country_mismatch", scored[0]["fraud_reasons"])

    def test_velocity_spike_detected(self):
        rows = [
            {
                "transaction_id": f"TXN-{i}",
                "customer_id": "C1",
                "event_ts": f"2026-01-01T10:0{i}:00+00:00",
                "amount": "100.00",
                "billing_country": "US",
                "ip_country": "US",
                "status": "approved",
            }
            for i in range(4)
        ]
        scored = detect_fraud(rows, high_value_threshold=500)
        self.assertIn("velocity_spike", scored[-1]["fraud_reasons"])


if __name__ == "__main__":
    unittest.main()
