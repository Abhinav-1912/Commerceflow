-- Daily GMV and order volume
SELECT
  DATE(timestamp) AS order_date,
  COUNT(*) AS orders,
  SUM(transaction_amount) AS gmv
FROM analytics.fact_transactions
GROUP BY DATE(timestamp)
ORDER BY order_date;

-- Top countries by revenue
SELECT
  country,
  SUM(transaction_amount) AS revenue
FROM analytics.fact_transactions
GROUP BY country
ORDER BY revenue DESC;
