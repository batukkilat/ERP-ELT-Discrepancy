from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta, datetime
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.operators.dummy_operator import DummyOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'One-pipline',
    default_args=default_args,
    description='Ingest data from sources then run DBT models',
    schedule_interval=timedelta(days=1),
    catchup=False
)
# task
dbtmodel = BashOperator(
    task_id='dbt-run',
    bash_command=' && '.join([
            'cd /opt/airflow/dags/dbt-profiles',
            'export DBT_PROFILES_DIR=$(pwd)',
            'cd ../dbt-project',
            # 'dbt test',
            'dbt run',
    ]),
    dag=dag
)


# Define tasks
ingest_erp = AirbyteTriggerSyncOperator(
    task_id='ingest-sql-to-citus',
    airbyte_conn_id='airbyte_conn',
    connection_id='1484321b-27df-42c2-bdd0-9bdb893bf1c4',
    asynchronous=False,
    timeout=3600,
    wait_seconds=3,
    dag=dag,
)


ingest_product_csv = AirbyteTriggerSyncOperator(
    task_id='ingest-product_csv-to-citus',
    airbyte_conn_id='airbyte_conn',
    connection_id='bd8504c1-20d0-453a-a5c7-bffa785e2ee2',
    asynchronous=False,
    timeout=3600,
    wait_seconds=3,
    dag=dag,
)

ingest_sales_csv = AirbyteTriggerSyncOperator(
    task_id='ingest-sales_csv-to-citus',
    airbyte_conn_id='airbyte_conn',
    connection_id='813304ae-574f-4f3e-9d40-42c5895d4f95',
    asynchronous=False,
    timeout=3600,
    wait_seconds=3,
    dag=dag,
)

ingest_sales_item_csv = AirbyteTriggerSyncOperator(
    task_id='ingest-sales_item_csv-to-citus',
    airbyte_conn_id='airbyte_conn',
    connection_id='1c96b05e-2582-46d8-8261-4fb5691d46dc',
    asynchronous=False,
    timeout=3600,
    wait_seconds=3,
    dag=dag,
)

end_task = DummyOperator(
    task_id='end_task',
    dag=dag,
)


ingest_erp >> dbtmodel
ingest_sales_csv >> dbtmodel
ingest_product_csv >> dbtmodel
ingest_sales_item_csv >> dbtmodel >> end_task