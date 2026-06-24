-- Example COPY command for loading curated data from S3 into Redshift
copy commerceflow.stg_transactions
from 's3://<your-curated-bucket>/transactions/'
iam_role '<your-redshift-iam-role-arn>'
format as parquet
region 'us-east-1';
