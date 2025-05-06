import logging
from airflow.decorators import dag, task
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

@dag(
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    default_args={
        "owner": "Arthur",
        "retries": 1,
        "retry_delay": timedelta(minutes=2),
    },
    tags=["spark", "teste"],
)
def teste_spark_submit_dag() -> None:
    """
    DAG de teste para execução de um job Spark via SparkSubmitOperator.
    """

    @task
    def log_inicio():
        logging.info("[teste_spark_submit_dag] Iniciando DAG de teste do Spark")

    spark_submit = SparkSubmitOperator(
        task_id="executa_job_spark",
        application="/opt/airflow/spark_jobs/teste_spark.py",  # Caminho dentro do container
        conn_id="spark_default",
        conf={
            # memória e cores mínimos
            "spark.driver.memory": "512m",
            "spark.executor.memory": "512m",
            "spark.executor.cores": "1",
        },
    )

    log_inicio() >> spark_submit


dag_instance = teste_spark_submit_dag()