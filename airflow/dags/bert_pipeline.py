import sys
from datetime import datetime, timedelta

from airflow.providers.standard.operators.python import PythonOperator
from airflow import DAG

prediction_project_path = '/opt/airflow/prediction_project'
sys.path.insert(0, prediction_project_path)

from workers.worker import Worker

default_args = {
    'owner': 'Mikhail',
    'start_date': datetime(2025, 11, 26),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_worker_pipeline():
    try:
        worker = Worker()

        input_path = '/opt/airflow/data/raw/reviews.csv'
        output_path = '/opt/airflow/data/processed/processed_reviews.csv'

        worker.run(input_path, output_path)

        return "Worker completed successfully"

    except Exception as e:
        print(f"Error in worker: {e}")
        raise

with DAG(
    'sentiment_worker_pipeline',
    default_args=default_args,
    description='Запуск Worker для анализа тональности',
    schedule=timedelta(minutes=5),
    catchup=False,
    tags={'sentiment', 'worker'},
) as dag:

    run_worker = PythonOperator(
        task_id='run_worker_pipeline',
        python_callable=run_worker_pipeline,
    )

    run_worker