from typing import List

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from prediction_project.logger import get_logger

logger = get_logger(__name__)

class BertModel:
    """
    Модель для анализа тональности текста с использованием BERT.
    """
    def __init__(self, model_name:str="cointegrated/rubert-tiny-sentiment-balanced"):
        """
        Инициализирует модель и токенизатор.
        :param model_name: Название модели из HuggingFace Hub.
            По умолчанию 'cointegrated/rubert-tiny-sentiment-balanced'.
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if not torch.cuda.is_available():
            logger.warning("Используется CPU вместо GPU")
        logger.info("Создан объект BertModel с моделью: %s", model_name)

    def load_model(self):
        """
        Метод загружает модель и токенизатор.
        """
        logger.info("Загрузка модели: %s", self.model_name)
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.model.eval()
            logger.debug("Модель загружена успешно")
        except Exception as e:
            logger.error("Ошибка загрузки модели: %s", e, exc_info=True)
            raise
        self.model.to(self.device)
        logger.debug("Модель загружена в память")

    def predict(self, text: str) -> float:
        """
        Предсказывает тональность для текста.
        :param text: Текст для анализа
        :return: score тональности от -1 (негатив) до 1 (позитив)
        """
        with torch.no_grad():
            logger.debug("Предсказание для текста длиной %d символов", len(text))

            try:
                inputs = self.tokenizer(text,
                                        return_tensors='pt',
                                        truncation=True,
                                        padding=True,
                                        max_length=512)
                output = self.model(**inputs).logits
                proba = torch.sigmoid(output)
                proba = proba.cpu()

                score_tensor = proba.matmul(torch.Tensor([-1, 0, 1]))
                score = score_tensor.item()
                score = round(score, 3)
                logger.info("Предсказание завершено. Score: %.3f ", score)
                return score

            except Exception as e:
                logger.error("Ошибка предсказания: %s", e, exc_info=True)
            raise

    def predict_batch(self, texts: List[str]) -> List[float]:
        """
        Предсказывает тональность для списка текстов.
        :param texts: Список текстов для анализа
        :return: Список скоров для текстов
        """
        logger.info("Начало инференса модели")
        scores = []
        for text in texts:
            score = self.predict(text)
            scores.append(score)
        return scores