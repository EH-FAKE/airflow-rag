import os
import json
import logging
from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from bs4 import BeautifulSoup

MINIO_CONN_ID = "minio_conn"
BUCKET_NAME = os.getenv("MINIO_BUCKET", "ragflow-lakehouse")
RAW_PREFIX = "raw/"


@dag(
    dag_id="raw_to_bronze_news_dag",
    schedule_interval=None,
    start_date=datetime(2025, 5, 1),
    catchup=False,
    default_args={
        "owner": "Arthur",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["bronze", "news"],
)
def raw_to_bronze_news_dag():

    @task
    def list_raw_keys() -> list[str]:
        hook = S3Hook(aws_conn_id=MINIO_CONN_ID)
        client = hook.get_conn()
        resp = client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=RAW_PREFIX)
        keys = [
            obj["Key"]
            for obj in resp.get("Contents", [])
            if obj["Key"].endswith(".html")
        ]
        logging.info(f"[list_raw_keys] HTMLs brutos encontrados: {keys}")
        return keys

    @task
    def parse_and_save(key: str) -> str:
        hook = S3Hook(aws_conn_id=MINIO_CONN_ID)
        html = hook.read_key(key, bucket_name=BUCKET_NAME)
        soup = BeautifulSoup(html, "html.parser")

        title = soup.title.string if soup.title else ""
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        slug = key.split("/")[-1].removesuffix(".html")

        # grava em JSON na camada bronze
        bronze_key = f"bronze/{slug}.json"
        record = {
            "slug": slug,
            "title": title,
            "paragraphs": paragraphs,
        }
        hook.load_string(
            string_data=json.dumps(record, ensure_ascii=False, indent=2),
            key=bronze_key,
            bucket_name=BUCKET_NAME,
            replace=True,
        )
        logging.info(f"[parse_and_save] Gravado JSON em s3://{BUCKET_NAME}/{bronze_key}")
        return bronze_key

    raw_keys = list_raw_keys()
    parse_and_save.expand(key=raw_keys)


dag = raw_to_bronze_news_dag()
