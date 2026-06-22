from airflow.sdk import dag, task
from datetime import datetime, timedelta
from extract import extract
from load import load

default_args = {
    'owner': 'Cliffe',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    }

@dag(
    'binance_batch_pipeline',
    default_args=default_args,
    description='Batch extraction and load for the Binance pipeline',
    start_date=datetime(2026, 6, 16),
    schedule='@daily',
    max_active_runs=1,
    catchup=False
    )

def binance_batch_pipeline():

    @task(task_id='binance_pipeline')
    def main():
        load()

    main()

binance_batch_pipeline()
