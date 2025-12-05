FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY prediction_project/ ./prediction_project/
COPY main.py .
COPY data/ ./data

CMD ["python", "main.py"]