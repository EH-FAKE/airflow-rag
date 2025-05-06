import os
import logging
from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator

MINIO_CONN_ID = "minio_conn"
BUCKET_NAME = os.getenv("MINIO_BUCKET", "ragflow-lakehouse")


@dag(
    dag_id="teste_minio_bucket_dag",
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    default_args={
        "owner": "Arthur",
        "retries": 1,
        "retry_delay": timedelta(minutes=2),
    },
    tags=["minio", "s3", "test"],
)
def teste_minio_bucket_dag():

    @task
    def log_inicio():
        logging.info("[teste_minio_bucket_dag] Iniciando teste de conexão com MinIO/S3")
    
    @task
    def listar_buckets() -> list[str]:
        hook = S3Hook(aws_conn_id=MINIO_CONN_ID)
        client = hook.get_conn()
        resp = client.list_buckets()
        buckets = [b["Name"] for b in resp.get("Buckets", [])]
        logging.info(f"[teste_minio_bucket_dag] Buckets existentes: {buckets}")
        return buckets

    criar_bucket = S3CreateBucketOperator(
        task_id="criar_bucket",
        bucket_name=BUCKET_NAME,
        aws_conn_id=MINIO_CONN_ID,
    )

    log_inicio() >> listar_buckets() >> criar_bucket


dag_instance = teste_minio_bucket_dag()