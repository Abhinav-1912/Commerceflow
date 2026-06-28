-- Core warehouse schema
create schema if not exists commerceflow;

create table if not exists commerceflow.dim_customers (
  customer_id varchar(50) primary key,
  first_name varchar(100),
  last_name varchar(100),
  email varchar(255),
  country varchar(20),
  signup_date date
);

create table if not exists commerceflow.fact_transactions (
  transaction_id varchar(50) primary key,
  customer_id varchar(50),
  transaction_ts timestamp,
  transaction_date date,
  amount decimal(18,2),
  currency varchar(10),
  payment_method varchar(20),
  ip_address varchar(50),
  device_id varchar(50),
  status varchar(20),
  country varchar(20),
  is_high_value int
);

-- Staging tables for COPY from S3
create table if not exists commerceflow.stg_dim_customers (
  customer_id varchar(50),
  first_name varchar(100),
  last_name varchar(100),
  email varchar(255),
  country varchar(20),
  signup_date date
);

create table if not exists commerceflow.stg_fact_transactions (
  transaction_id varchar(50),
  customer_id varchar(50),
  transaction_ts timestamp,
  transaction_date date,
  amount decimal(18,2),
  currency varchar(10),
  payment_method varchar(20),
  ip_address varchar(50),
  device_id varchar(50),
  status varchar(20),
  country varchar(20),
  is_high_value int
);
