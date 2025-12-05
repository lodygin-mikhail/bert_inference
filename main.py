from prediction_project.constants.constants import RAW_DATA, PROCESSED_DATA
from prediction_project.workers.worker import Worker

if __name__ == "__main__":
    worker = Worker()
    worker.initialize()
    worker.run(RAW_DATA, PROCESSED_DATA)