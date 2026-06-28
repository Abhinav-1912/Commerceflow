-- Daily revenue KPI
select
  transaction_date,
  sum(amount) as daily_revenue,
  count(*) as total_transactions,
  sum(case when status = 'COMPLETED' then 1 else 0 end) as completed_transactions
from commerceflow.fact_transactions
group by transaction_date
order by transaction_date;

-- Top customers by spend
select
  customer_id,
  sum(amount) as total_spend,
  count(*) as tx_count
from commerceflow.fact_transactions
where status = 'COMPLETED'
group by customer_id
order by total_spend desc
limit 20;
