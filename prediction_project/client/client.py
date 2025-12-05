import pandas as pd

from prediction_project.logger import get_logger

logger = get_logger(__name__)

class FileClient:
    """
    Клиент для работы с файловой системой.
    """
    def read(self, file_path: str) -> pd.DataFrame:
        """
        Метод преобразует CSV файл в pandas.DataFrame
        :param file_path: Путь к исходному файлу CSV с данными
        :return: pandas.DataFrame
        """
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

    def write(self, data: pd.DataFrame, file_path: str):
        """
        Метод записывает pandas.DataFrame в CSV файл по указанному пути
        :param data: Данные pandas.DataFrame
        :param file_path: Путь для записи CSV файла
        :return:
        """
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