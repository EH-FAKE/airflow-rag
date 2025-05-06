import os
import logging
import requests

from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

MINIO_CONN_ID = "minio_conn"
BUCKET_NAME = os.getenv("MINIO_BUCKET", "ragflow-lakehouse")

@dag(
    dag_id="raw_news_fetch_dag",
    schedule_interval=None,
    start_date=datetime(2025, 5, 1),
    catchup=False,
    default_args={
        "owner": "Arthur",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["raw", "news"],
)
def raw_news_fetch_dag():
    """
    DAG de ingestão Raw: baixa o HTML de uma notícia
    e salva em raw/{slug}
    """

    @task
    def fetch_html(url: str) -> str:
        logging.info(f"📥 Buscando HTML de {url}")
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.text

    @task
    def save_to_s3(html: str, url: str) -> str:
        hook = S3Hook(aws_conn_id=MINIO_CONN_ID)
        slug = url.rstrip("/").split("/")[-1] + ".html"
        key = f"raw/{slug}"
        hook.load_string(
            string_data=html,
            key=key,
            bucket_name=BUCKET_NAME,
            replace=True
        )
        logging.info(f"✅ HTML salvo em s3://{BUCKET_NAME}/{key}")
        return key

    news_url = (
        "https://g1.globo.com/sp/santos-regiao/noticia/"
        "2025/05/01/chefe-que-tomou-carro-de-funcionaria-e-foi-preso-"
        "pela-pf-se-apresentava-como-amigo-de-neymar-entenda.ghtml"
    )

    html = fetch_html(news_url)
    save_to_s3(html, news_url)

dag = raw_news_fetch_dag()