import os
import boto3


def get_s3_client(region: str | None = None):
    return boto3.client("s3", region_name=region or os.getenv("AWS_REGION", "us-east-1"))


def get_redshift_data_client(region: str | None = None):
    return boto3.client("redshift-data", region_name=region or os.getenv("AWS_REGION", "us-east-1"))
