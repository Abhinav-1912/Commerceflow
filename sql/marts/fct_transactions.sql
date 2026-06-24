-- Curated transaction fact table
create table if not exists commerceflow.fct_transactions as
select
    transaction_id,
    customer_id,
    event_ts,
    cast(amount as decimal(12,2)) as amount,
    currency,
    payment_method,
    billing_country,
    ip_country,
    device_id,
    status,
    case when cast(amount as decimal(12,2)) >= 500 then true else false end as is_high_value,
    case when billing_country <> ip_country then true else false end as is_country_mismatch
from commerceflow.stg_transactions;
