import pandas as pd

from logger import get_logger

logger = get_logger(__name__)

class FileClient:

    def read_file(self, file_path):
        try:
            logger.info("Загрузка данных из %s", file_path)
            data = pd.read_csv(file_path)
            logger.info("Успешно загружено %d записей", len(data))
            return data
        except FileNotFoundError:
            logger.error("Файл не найден: %s", file_path)
            raise
        except Exception as e:
            logger.error("Ошибка загрузки данных: %s", e, exc_info=True)
            raise

    def write_file(self, data, file_path):
        try:
            logger.info("Выгрузка данных в %s", file_path)
            data.to_csv(file_path, index=False)
            logger.info("Успешно выгружены %d записей", len(data))
        except FileNotFoundError:
            logger.error("Файл не найден: %s", file_path)
            raise
        except Exception as e:
            logger.error("Ошибка загрузки данных: %s", e, exc_info=True)
            raise