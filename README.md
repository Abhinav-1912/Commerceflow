# CommerceFlow

CommerceFlow is a runnable data engineering project scaffold for e-commerce transactions. It demonstrates an end-to-end ETL pipeline (ingest → clean → transform → validate) with a local-first workflow and AWS Glue/S3/Redshift-compatible configuration.

## Project structure

```text
Commerceflow/
├── config/
│   ├── aws_glue_redshift.example.json
│   └── local.example.json
├── data/
│   ├── raw/
│   └── processed/
│       ├── bronze/
│       ├── silver/
│       └── gold/
├── scripts/
│   └── run_local_pipeline.py
├── sql/
│   ├── analytics_queries.sql
│   └── fraud_detection_queries.sql
├── src/
│   └── commerceflow/
│       ├── cleaning.py
│       ├── cli.py
│       ├── config.py
│       ├── generator.py
│       ├── ingestion.py
│       ├── pipeline.py
│       ├── transformation.py
│       └── validation.py
└── tests/
    └── test_pipeline.py
```

## What it does

- Generates sample e-commerce transactions locally when input is missing.
- Cleans invalid records (bad timestamp, non-positive quantity/price, missing IDs).
- Transforms records with business fields:
  - `transaction_amount`
  - `is_high_value`
  - `is_suspicious` (high-value COD)
- Validates schema + business rules (duplicate IDs, amount mismatch, invalid values).
- Writes layered outputs:
  - Bronze: raw input rows
  - Silver: cleaned rows
  - Gold: transformed + validated rows

## Run locally

From repository root (`/home/runner/work/Commerceflow/Commerceflow`):

```bash
PYTHONPATH=src python scripts/run_local_pipeline.py --config config/local.example.json
```

Expected output is a JSON summary with row counts and output file locations.

## Run tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## AWS integration (example)

`config/aws_glue_redshift.example.json` contains placeholders for:

- S3 raw/curated buckets
- Glue job name
- Redshift target table

Use these values in your Glue ETL job and Redshift load process while keeping this repository runnable without AWS credentials.

## SQL analytics and fraud queries

- `sql/analytics_queries.sql` for GMV and country-level revenue
- `sql/fraud_detection_queries.sql` for suspicious-transaction investigations

Point the queries to your Redshift schema/table (example: `analytics.fact_transactions`).
