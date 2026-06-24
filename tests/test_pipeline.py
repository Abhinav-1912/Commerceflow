import unittest

from commerceflow.cleaning import clean_transactions
from commerceflow.transformation import transform_transactions
from commerceflow.validation import validate_transactions


class TestTransactionPipeline(unittest.TestCase):
    def test_cleaning_filters_invalid_rows(self):
        raw = [
            {
                "transaction_id": "txn_1",
                "customer_id": "cust_1",
                "timestamp": "2026-01-01T00:00:00",
                "product_id": "prod_1",
                "quantity": "2",
                "unit_price": "10.5",
                "payment_method": "card",
                "country": "us",
            },
            {
                "transaction_id": "txn_2",
                "customer_id": "cust_2",
                "timestamp": "bad-time",
                "product_id": "prod_2",
                "quantity": "1",
                "unit_price": "1",
                "payment_method": "card",
                "country": "us",
            },
        ]

        cleaned = clean_transactions(raw)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned[0]["country"], "US")

    def test_transformation_flags_suspicious_cod_high_value(self):
        cleaned = [
            {
                "transaction_id": "txn_1",
                "customer_id": "cust_1",
                "timestamp": "2026-01-01T00:00:00",
                "product_id": "prod_1",
                "quantity": 2,
                "unit_price": 600.0,
                "payment_method": "cod",
                "country": "US",
            }
        ]

        transformed = transform_transactions(cleaned)
        self.assertEqual(transformed[0]["transaction_amount"], 1200.0)
        self.assertEqual(transformed[0]["is_high_value"], 1)
        self.assertEqual(transformed[0]["is_suspicious"], 1)

    def test_validation_catches_duplicate_ids(self):
        rows = [
            {
                "transaction_id": "txn_1",
                "customer_id": "cust_1",
                "timestamp": "2026-01-01T00:00:00",
                "product_id": "prod_1",
                "quantity": 1,
                "unit_price": 100.0,
                "payment_method": "card",
                "country": "US",
                "transaction_amount": 100.0,
                "is_high_value": 0,
                "is_suspicious": 0,
            },
            {
                "transaction_id": "txn_1",
                "customer_id": "cust_2",
                "timestamp": "2026-01-01T00:01:00",
                "product_id": "prod_2",
                "quantity": 1,
                "unit_price": 200.0,
                "payment_method": "card",
                "country": "US",
                "transaction_amount": 200.0,
                "is_high_value": 0,
                "is_suspicious": 0,
            },
        ]

        valid, errors = validate_transactions(rows)
        self.assertFalse(valid)
        self.assertTrue(any("duplicate transaction_id" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
