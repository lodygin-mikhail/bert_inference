import sys
from datetime import datetime, timedelta

from airflow.providers.standard.operators.python import PythonOperator
from airflow import DAG

prediction_project_path = '/opt/airflow/prediction_project'
sys.path.insert(0, prediction_project_path)

from client.client import FileClient
from predict.predict import BertModel
from processing.processor import Processor

default_args = {
    'owner': 'Mikhail',
    'start_date': datetime(2025, 1, 1),
    'email': 'lodygin-mikhail@mail.ru',
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

client = FileClient()
processor = Processor()

def extract_data(**context):

    data = client.read_file('/opt/airflow/data/raw/reviews.csv')
    context['ti'].xcom_push(key='raw_data', value=data)
    return 'Data extracted successfully'

def preprocess_data(**context):
    data = context['ti'].xcom_pull(task_ids='extract_data', key='raw_data')
    processed_data = processor.preprocess_data(data)
    context['ti'].xcom_push(key='processed_data', value=processed_data)
    return 'Data preprocessed successfully'

def model_predict(**context):
    data = context['ti'].xcom_pull(task_ids='preprocess_data', key='processed_data')
    model = BertModel()
    predicted_data = model.predict(data)
    context['ti'].xcom_push(key='predicted_data', value=predicted_data)
    return 'Predictions done successfully'

def postprocess_data(**context):
    data = context['ti'].xcom_pull(task_ids='model_predict', key='predicted_data')
    processed_data = processor.postprocess_data(data)
    context['ti'].xcom_push(key='postprocessed_data', value=processed_data)
    return 'Data postprocessed successfully'

def load_data(**context):
    data = context['ti'].xcom_pull(task_ids='postprocess_data', key='postprocessed_data')
    client.write_file(data, '/opt/airflow/data/processed/processed_reviews.csv')
    return 'Data loaded successfully'

with DAG(
    dag_id='milti_task_dag',
    default_args=default_args,
    description='Пайплайн загрузки, предобработки и оценки тональности отзывов на фильмы',
    schedule=timedelta(minutes=5),
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags={'sentiment analysis', 'BERT'},
) as dag:

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    preprocess_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data,
    )

    model_predict_task = PythonOperator(
        task_id='model_predict',
        python_callable=model_predict,
    )

    postprocess_task = PythonOperator(
        task_id='postprocess_data',
        python_callable=postprocess_data,
    )

    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )

    extract_task >> preprocess_task >> model_predict_task >> postprocess_task >> load_data_task