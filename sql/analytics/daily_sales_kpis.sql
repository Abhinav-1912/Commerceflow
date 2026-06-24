-- Daily business KPIs
select
    date_trunc('day', event_ts) as order_date,
    count(*) as total_transactions,
    sum(amount) as gross_sales,
    avg(amount) as avg_order_value,
    sum(case when status = 'approved' then amount else 0 end) as approved_sales,
    sum(case when status = 'declined' then 1 else 0 end) as declined_count
from commerceflow.fct_transactions
group by 1
order by 1 desc;
