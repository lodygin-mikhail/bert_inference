from prediction_project.logger import get_logger
from prediction_project.client.client import FileClient
from prediction_project.processing.processor import Processor
from prediction_project.model.model import BertModel

logger = get_logger(__name__)


class Worker:
    """
    Координатор ETL пайплайна для анализа тональности.
    """
    def __init__(self):
        """
        Инициализирует экземпляры классов Client, Processor, BertModel.
        """
        self.client = None
        self.processor = None
        self.model = None
        logger.info("Создан объект класса Worker")

    def initialize(self):
        """
        Метод иницализирует воркера.
        :return:
        """
        logger.info("Инициализация воркера")
        try:
            self.client = FileClient()
            self.processor = Processor()
            self.model = BertModel()
            self.model.load_model()
            logger.debug("Воркер успешно инициализирован")
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
            data = self.client.read(input_path)
            processed_data = self.processor.preprocess_data(data)
            processed_data['scores'] = self.model.predict_batch(processed_data.review.tolist())
            postprocessed_data = self.processor.postprocess_data(processed_data)
            self.client.write(postprocessed_data, output_path)
            logger.info("Успешное выполнение воркера")

        except Exception as e:
            logger.error("Ошибка выполнения воркера: %s", e, exc_info=True)
            raise
