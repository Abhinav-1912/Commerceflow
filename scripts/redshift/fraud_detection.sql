-- Simple fraud heuristics
-- 1) High-value transactions
select *
from commerceflow.fact_transactions
where is_high_value = 1
order by amount desc;

-- 2) Rapid successive purchases by same customer in 10-minute windows
select
  a.customer_id,
  a.transaction_id as tx1,
  b.transaction_id as tx2,
  a.transaction_ts as ts1,
  b.transaction_ts as ts2,
  a.amount as amount1,
  b.amount as amount2
from commerceflow.fact_transactions a
join commerceflow.fact_transactions b
  on a.customer_id = b.customer_id
 and a.transaction_id <> b.transaction_id
 and datediff(minute, a.transaction_ts, b.transaction_ts) between 0 and 10
where a.status = 'COMPLETED' and b.status = 'COMPLETED'
order by a.customer_id, a.transaction_ts;

-- 3) Multiple high-value transactions from same device
select
  device_id,
  count(*) as high_value_tx_count,
  sum(amount) as high_value_total
from commerceflow.fact_transactions
where is_high_value = 1 and status = 'COMPLETED'
group by device_id
having count(*) >= 2
order by high_value_total desc;
