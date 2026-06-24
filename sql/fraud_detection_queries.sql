-- High-value cash-on-delivery transactions
SELECT
  transaction_id,
  customer_id,
  timestamp,
  transaction_amount,
  payment_method,
  country
FROM analytics.fact_transactions
WHERE is_high_value = 1
  AND payment_method = 'cod';

-- Customer fraud risk score based on suspicious order counts
SELECT
  customer_id,
  COUNT(*) AS suspicious_transactions,
  SUM(transaction_amount) AS suspicious_amount
FROM analytics.fact_transactions
WHERE is_suspicious = 1
GROUP BY customer_id
ORDER BY suspicious_amount DESC;
