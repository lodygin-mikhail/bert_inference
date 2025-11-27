from pathlib import Path

from prediction_project.workers.worker import Worker

PROJECT_PATH = Path(__file__).parent
DATA_PATH = PROJECT_PATH / 'data'

if __name__ == "__main__":
    worker = Worker()
    worker.run(DATA_PATH / 'raw' / 'reviews.csv', DATA_PATH / 'processed' / 'processed_reviews.csv')