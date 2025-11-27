import pandas as pd

from logger import get_logger

logger = get_logger(__name__)

class Processor:

    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
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
        """23.04.2025 -> 23/04/2025"""
        return number.replace(".", "/")