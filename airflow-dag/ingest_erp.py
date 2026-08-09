from datetime import datetime, timedelta
from airflow import DAG
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
    'ingest_to_citus',
    default_args=default_args,
    description='A DAG to ingest data into Citus using Airbyte',
    schedule_interval=timedelta(days=1)

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

# task dependencies
ingest_erp >> ingest_sales_csv >> ingest_product_csv >> ingest_sales_item_csv >> end_task