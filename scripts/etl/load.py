from __future__ import annotations

import time

from utils.aws_clients import get_redshift_data_client
from utils.logger import get_logger

logger = get_logger(__name__)


def execute_redshift_sql(sql: str) -> None:
    client = get_redshift_data_client()

    cluster_id = __import__("os").getenv("REDSHIFT_CLUSTER_ID")
    workgroup = __import__("os").getenv("REDSHIFT_WORKGROUP_NAME")
    database = __import__("os").getenv("REDSHIFT_DATABASE", "dev")
    db_user = __import__("os").getenv("REDSHIFT_DB_USER")
    secret_arn = __import__("os").getenv("REDSHIFT_SECRET_ARN")

    params = {
        "Database": database,
        "Sql": sql,
    }

    if cluster_id:
        params["ClusterIdentifier"] = cluster_id
        if secret_arn:
            params["SecretArn"] = secret_arn
        elif db_user:
            params["DbUser"] = db_user
        else:
            raise ValueError("Set REDSHIFT_SECRET_ARN or REDSHIFT_DB_USER for provisioned cluster")
    elif workgroup:
        params["WorkgroupName"] = workgroup
        if secret_arn:
            params["SecretArn"] = secret_arn
    else:
        raise ValueError("Set REDSHIFT_CLUSTER_ID or REDSHIFT_WORKGROUP_NAME")

    resp = client.execute_statement(**params)
    statement_id = resp["Id"]

    while True:
        desc = client.describe_statement(Id=statement_id)
        status = desc["Status"]
        if status in {"FINISHED", "FAILED", "ABORTED"}:
            break
        time.sleep(1)

    if status != "FINISHED":
        raise RuntimeError(f"Redshift SQL failed: {desc.get('Error')}")

    logger.info("Executed SQL statement: %s", statement_id)
