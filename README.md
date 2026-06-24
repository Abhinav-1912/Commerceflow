# CommerceFlow

CommerceFlow is a complete, portfolio-ready e-commerce data engineering project demonstrating an end-to-end transaction pipeline using Python + SQL with AWS Glue/S3/Redshift integration templates.

## Architecture

1. **Data simulation (Python)** generates realistic transaction events.
2. **Raw zone (S3-compatible local folder)** stores JSONL transaction events.
3. **ETL + fraud scoring (Python / Glue-ready)** cleans and enriches records.
4. **Warehouse load (Redshift SQL + local SQLite demo)** supports analytics queries.
5. **Business + fraud analytics (SQL)** power KPI and risk monitoring.

```text
Simulator -> Raw (JSONL in S3/local) -> ETL/Fraud -> Curated CSV/Parquet -> Redshift marts -> Analytics SQL
```

## Project Structure

```text
configs/
  .env.example
infra/aws/
  glue_job_template.py
  redshift_copy_example.sql
sql/
  staging/stg_transactions.sql
  marts/fct_transactions.sql
  analytics/daily_sales_kpis.sql
  analytics/fraud_candidates.sql
src/commerceflow/
  config.py
  data_simulation.py
  etl.py
  fraud.py
  io.py
  pipeline.py
  cli.py
tests/
  test_etl.py
  test_fraud.py
data/sample/
  transactions_sample.jsonl
```

## Local Setup

```bash
cd /home/runner/work/Commerceflow/Commerceflow
python -m venv .venv
source .venv/bin/activate
export PYTHONPATH=src
cp configs/.env.example .env
```

## Run the Pipeline

```bash
export PYTHONPATH=src
python -m commerceflow.cli --transactions 500 --seed 42
```

Outputs are written to `data/output/`:
- `raw/transactions.jsonl`
- `curated/transactions_scored.csv`
- `warehouse/commerceflow.db`

## Run Tests

```bash
export PYTHONPATH=src
python -m unittest discover -s tests -v
```

## AWS Integration Notes

- **Glue**: Use `infra/aws/glue_job_template.py` as a starting ETL job script.
- **S3**: Configure `CF_S3_RAW_BUCKET` and `CF_S3_CURATED_BUCKET` via environment variables.
- **Redshift**:
  - Create stage + marts with scripts in `sql/staging` and `sql/marts`.
  - Load curated files from S3 using `infra/aws/redshift_copy_example.sql`.

## Data Flow

- Simulator creates transaction records with IDs, timestamps, amounts, payment attributes, and geography.
- ETL standardizes numeric/time fields and adds high-value flags.
- Fraud module assigns risk score using high amount, country mismatch, payment failures, and customer velocity.
- SQL analytics provides daily sales KPIs and candidate fraud investigations.

## Portfolio Highlights

- End-to-end data engineering lifecycle (ingest -> transform -> warehouse -> analytics).
- Cloud-ready design with local execution fallback.
- Modular, testable Python code and practical SQL artifacts.
