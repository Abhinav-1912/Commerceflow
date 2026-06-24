-- Redshift staging model for raw transactions loaded from S3
create table if not exists commerceflow.stg_transactions (
    transaction_id varchar(32) encode zstd,
    customer_id varchar(32) encode zstd,
    event_ts timestamp encode zstd,
    amount decimal(12,2) encode az64,
    currency varchar(8) encode zstd,
    payment_method varchar(32) encode zstd,
    billing_country varchar(8) encode zstd,
    ip_country varchar(8) encode zstd,
    device_id varchar(32) encode zstd,
    status varchar(16) encode zstd,
    ingestion_ts timestamp default getdate()
)
diststyle auto
sortkey(event_ts);
