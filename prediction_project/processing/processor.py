import pandas as pd

from logger import get_logger

logger = get_logger(__name__)

class Processor:
    """
        Обработчик текстовых данных для ML пайплайна.
        Выполняет предобработку текста перед подачей в модель и
        постобработку предсказаний для финального результата.
    """
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Метод предобрабатывает данные перед передачей в модель.
        :param data: Данные после загрузки с диска
        :return: pd.DataFrame
        """
        try:
            logger.debug("Начало предобработки данных")
            logger.info("Предобработка %d записей", len(data))

            data["review_date"] = data["review_date"].apply(self.process_date)

            logger.info("Обработано %d записей", len(data))
            return data
        except Exception as e:
            logger.error("Ошибка предобработки данных: %s", e, exc_info=True)
            raise

    def postprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Метод выполняет постобработку данных после модели. Для каждого скора добавляется лейбл тональности.
        :param data: pd.DataFrame
        :return: pd.DataFrame
        """
        try:
            logger.debug("Начало постобработки данных")
            logger.info("Постобработка %d записей", len(data))

            bins = [-float('inf'), -0.3, 0.3, float('inf')]
            labels = ['negative', 'neutral', 'positive']

            data['label'] = pd.cut(data['scores'], bins=bins, labels=labels)
            logger.info("Обработано %d записей", len(data))
            return data
        except Exception as e:
            logger.error("Ошибка постобработки данных: %s", e, exc_info=True)
            raise

    @staticmethod
    def process_date(number: str) -> str:
        """
        Метод заменяет точки в дате на слэши.
        :param number: Дата dd.mm.yyyy
        :return: Дата dd/mm/yyyy
        """
        return number.replace(".", "/")