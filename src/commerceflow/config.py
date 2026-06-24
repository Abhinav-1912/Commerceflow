from dataclasses import dataclass
import os


def _get_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    project_name: str = os.getenv("CF_PROJECT_NAME", "commerceflow")
    output_dir: str = os.getenv("CF_OUTPUT_DIR", "data/output")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    s3_raw_bucket: str = os.getenv("CF_S3_RAW_BUCKET", "commerceflow-raw")
    s3_curated_bucket: str = os.getenv("CF_S3_CURATED_BUCKET", "commerceflow-curated")
    redshift_schema: str = os.getenv("CF_REDSHIFT_SCHEMA", "commerceflow")
    high_value_threshold: float = float(os.getenv("CF_HIGH_VALUE_THRESHOLD", "500"))
    fail_on_empty: bool = _get_bool("CF_FAIL_ON_EMPTY", False)
