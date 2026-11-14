import pendulum

from airflow.sdk import dag, task
from airflow.providers.standard.operators.bash import BashOperator


@dag(
    dag_id="tfl_data_pipeline",
    schedule="@hourly",
    start_date=pendulum.datetime(2026, 11, 14, tz="UTC"),
    catchup=False,
)
def tfl_data_pipeline():

    @task
    def ingest_tfl():
        from tfl_pipeline.pipeline import run_ingestion

        run_ingestion()

    ingest_task = ingest_tfl()

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="dbt run \
            --project-dir /opt/airflow/app/dbt \
            --profiles-dir /opt/airflow/app/dbt",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="dbt test \
            --project-dir /opt/airflow/app/dbt \
            --profiles-dir /opt/airflow/app/dbt",
    )

    ingest_task >> dbt_run >> dbt_test


tfl_data_pipeline()