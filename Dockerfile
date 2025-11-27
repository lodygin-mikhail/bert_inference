FROM apache/airflow:3.1.3

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && apt-get clean

USER airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY prediction_project/ /opt/airflow/prediction_project/