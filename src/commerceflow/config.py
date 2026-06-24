from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    raw_input_path: str
    bronze_output_path: str
    silver_output_path: str
    gold_output_path: str


@dataclass(frozen=True)
class AwsIntegrationConfig:
    s3_raw_uri: str
    s3_curated_uri: str
    glue_job_name: str
    redshift_table: str


def load_pipeline_config(path: str | Path) -> PipelineConfig:
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    return PipelineConfig(**data["pipeline"])


def load_aws_integration_config(path: str | Path) -> AwsIntegrationConfig:
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    return AwsIntegrationConfig(**data["aws_integration"])
