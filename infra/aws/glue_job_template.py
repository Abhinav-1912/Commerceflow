"""AWS Glue ETL job template for CommerceFlow.

This script is a deployment stub. Replace source/target paths with your AWS resources.
"""

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
import sys

args = getResolvedOptions(sys.argv, ["JOB_NAME", "RAW_S3_PATH", "CURATED_S3_PATH"])
sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

raw_df = spark.read.json(args["RAW_S3_PATH"])
curated_df = raw_df.dropDuplicates(["transaction_id"])  # Add transformations as needed
curated_df.write.mode("overwrite").parquet(args["CURATED_S3_PATH"])

job.commit()
