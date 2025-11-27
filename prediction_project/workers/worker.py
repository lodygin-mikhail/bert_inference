from logger import get_logger
from client.client import FileClient
from processing.processor import Processor
from predict.predict import BertModel

logger = get_logger(__name__)


class Worker:
    """
    Координатор ETL пайплайна для анализа тональности.
    """
    def __init__(self):
        """
        Инициализирует экземпляры классов Client, Processor, BertModel.
        """
        logger.info("Инициализация воркера: %s")
        try:
            self.client = FileClient()
            self.processor = Processor()
            self.model = BertModel()
        except Exception as e:
            logger.error("Ошибка инициализации воркера: %s", e, exc_info=True)
            raise

    def run(self, input_path:str, output_path:str):
        """
        Метод запускает полный пайплайн обработки отзывов.
        :param input_path: Путь до исходного файла CSV с данными.
        :param output_path: Путь сохранения данных в файле CSV.
        :return:
        """
        logger.info("Начало работы воркера")
        try:
            data = self.client.read_file(input_path)
            processed_data = self.processor.preprocess_data(data)
            model_prediction = self.model.predict(processed_data)
            postprocessed_data = self.processor.postprocess_data(model_prediction)
            self.client.write_file(postprocessed_data, output_path)
            logger.info("Успешное выполнение воркера")

        except Exception as e:
            logger.error("Ошибка выполнения воркера: %s", e, exc_info=True)
            raise
