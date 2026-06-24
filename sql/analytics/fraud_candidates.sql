-- SQL fraud candidate extraction for analyst review
with customer_velocity as (
    select
        t.*,
        count(*) over (
            partition by customer_id
            order by event_ts
            rows between 3 preceding and current row
        ) as tx_in_recent_window
    from commerceflow.fct_transactions t
)
select
    transaction_id,
    customer_id,
    event_ts,
    amount,
    billing_country,
    ip_country,
    status,
    case
        when amount >= 700 then 'high_amount'
        when billing_country <> ip_country then 'country_mismatch'
        when tx_in_recent_window >= 4 then 'velocity_spike'
        when status = 'declined' then 'declined_payment'
        else 'normal'
    end as fraud_signal
from customer_velocity
where amount >= 700
   or billing_country <> ip_country
   or tx_in_recent_window >= 4
   or status = 'declined';
