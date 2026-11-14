FROM apache/airflow:3.4.0

WORKDIR /opt/airflow/app

COPY --chown=airflow:root pyproject.toml .
COPY --chown=airflow:root src ./src
COPY --chown=airflow:root dbt/dbt_project.yml ./dbt/dbt_project.yml
COPY --chown=airflow:root dbt/models ./dbt/models
COPY --chown=airflow:root dbt/tests ./dbt/tests
COPY --chown=airflow:root dbt/profiles.airflow.yml ./dbt/profiles.yml

RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    -e ".[dev]"